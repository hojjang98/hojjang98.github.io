import os
import re

def should_keep_as_code(block_content):
    """실제 코드인지 판단"""
    code_indicators = [
        'import ', 'from ', 'def ', 'class ', 'function',
        'const ', 'let ', 'var ', 'if (', 'for (', 'while (',
        '#!/bin/', 'package ', 'public class', 'private ',
        'SELECT ', 'INSERT ', 'UPDATE ', 'DELETE ',
        '<html', '<div', '<script', '<?php',
        'return ', 'print(', 'console.', 'echo ',
        'npm install', 'pip install', 'git ', 'sudo ',
        'http://', 'https://', 'localhost:', 'curl ',
        'CMD', 'RUN', 'FROM', 'COPY', 'apt-get',
        '#!/', '.then(', '.catch(', 'async ', 'await ',
        '&&', '||', '==', '!=', '++', '--'
    ]
    
    content_lower = block_content.lower()
    matches = sum(1 for indicator in code_indicators if indicator.lower() in content_lower)
    
    return matches >= 2

def fix_all_diagram_blocks(content):
    """파일 내 모든 코드 블록 처리"""
    
    # 모든 코드 블록을 찾아서 하나씩 처리
    pattern = r'```\n(.*?)```'
    
    def replace_block(match):
        block = match.group(1)
        
        # 실제 코드면 유지
        if should_keep_as_code(block):
            return match.group(0)
        
        # 다이어그램 지표 확인
        diagram_indicators = ['├', '│', '└', '─', '↓', '→', '←', '↑', 
                            '[1단계]', '[2단계]', '[3단계]', '[4단계]', '[5단계]',
                            '[Stage', 'Phase', '┌', '┐', '┘', '┴', '┬',
                            '▶', '●', '○', '■', '□']
        
        has_diagram = any(indicator in block for indicator in diagram_indicators)
        
        if has_diagram:
            # 코드 블록 제거하고 줄 끝 스페이스 2개 추가
            lines = block.rstrip('\n').split('\n')
            fixed = [line.rstrip() + '  ' for line in lines if line.strip()]
            return '\n' + '\n'.join(fixed) + '\n\n'
        
        # 그 외는 유지
        return match.group(0)
    
    # re.DOTALL로 여러 줄 매칭, 모든 코드 블록 처리
    return re.sub(pattern, replace_block, content, flags=re.DOTALL)

def process_files(directory):
    count = 0
    total = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                total += 1
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if '```' in content:
                        original_blocks = content.count('```')
                        fixed = fix_all_diagram_blocks(content)
                        fixed_blocks = fixed.count('```')
                        
                        if fixed != content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(fixed)
                            print(f"✅ Fixed: {filepath} (코드블록: {original_blocks//2} → {fixed_blocks//2})")
                            count += 1
                        else:
                            print(f"⏭️  Kept: {filepath} (코드블록: {original_blocks//2}개 유지)")
                
                except Exception as e:
                    print(f"❌ Error: {filepath}: {e}")
    
    print(f"\n✨ {count}/{total} 파일 수정 완료!")

if __name__ == "__main__":
    process_files("content")