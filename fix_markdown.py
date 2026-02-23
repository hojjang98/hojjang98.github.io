import os
import re

def fix_all_code_blocks(content):
    """모든 코드 블록을 일반 텍스트로 변환 (실제 코드는 제외)"""
    
    # 코드 블록 패턴 찾기
    pattern = r'```\n((?:.*?\n)*?)```'
    
    def should_convert(block_content):
        """코드 블록을 변환해야 하는지 판단"""
        # 실제 코드 키워드가 있으면 변환하지 않음
        code_keywords = ['import', 'function', 'const', 'let', 'var', 'def', 'class', 
                        'if __name__', 'public', 'private', 'void', '{', '}', 'npm install']
        
        for keyword in code_keywords:
            if keyword in block_content:
                return False
        
        # 화살표나 다이어그램 같은 구조가 있으면 변환
        diagram_indicators = ['↓', '→', '←', '↑', '▶', '■', '□', '●', '○', 
                             'IDENTIFICATION', 'DATA SCREENING', 'DATA ANALYSIS',
                             '[1단계]', '[2단계]', '[3단계]', '[4단계]', '[5단계]']
        
        for indicator in diagram_indicators:
            if indicator in block_content:
                return True
        
        return False
    
    def replace_code_block(match):
        block_content = match.group(1)
        
        # 변환해야 하는 블록인지 확인
        if should_convert(block_content):
            # 각 줄 끝에 스페이스 2개 추가
            lines = block_content.split('\n')
            fixed_lines = [line.rstrip() + '  ' for line in lines if line.strip()]
            return '\n'.join(fixed_lines)
        else:
            # 코드 블록은 그대로 유지
            return match.group(0)
    
    fixed_content = re.sub(pattern, replace_code_block, content, flags=re.DOTALL)
    return fixed_content

def process_files(directory):
    """디렉토리 내 모든 .md 파일 처리"""
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 코드 블록이 있는 경우만 수정
                    if '```' in content:
                        fixed_content = fix_all_code_blocks(content)
                        
                        if fixed_content != content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(fixed_content)
                            print(f"✅ Fixed: {filepath}")
                            count += 1
                    
                except Exception as e:
                    print(f"❌ Error: {filepath}: {e}")
    
    print(f"\n✨ 총 {count}개 파일 수정 완료!")

if __name__ == "__main__":
    process_files("content")