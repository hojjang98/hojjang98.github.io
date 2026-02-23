import os
import re

def fix_code_blocks(content):
    """코드 블록을 일반 텍스트로 변환하고 줄 끝에 스페이스 2개 추가"""
    
    # ```로 시작하는 코드 블록 패턴 찾기
    pattern = r'```\n(\[연구 설계 구조\].*?)\n```'
    
    def replace_code_block(match):
        # 코드 블록 내용 추출
        content = match.group(1)
        # 각 줄 끝에 스페이스 2개 추가
        lines = content.split('\n')
        fixed_lines = [line.rstrip() + '  ' for line in lines if line.strip()]
        return '\n'.join(fixed_lines)
    
    # 코드 블록을 일반 텍스트로 변환
    fixed_content = re.sub(pattern, replace_code_block, content, flags=re.DOTALL)
    
    return fixed_content

def process_files(directory):
    """디렉토리 내 모든 .md 파일 처리"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 수정
                    fixed_content = fix_code_blocks(content)
                    
                    # 변경 사항이 있으면 저장
                    if fixed_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(fixed_content)
                        print(f"✅ Fixed: {filepath}")
                    
                except Exception as e:
                    print(f"❌ Error processing {filepath}: {e}")

# 실행
if __name__ == "__main__":
    content_dir = "content"  # Hugo의 content 디렉토리
    process_files(content_dir)
    print("\n✨ 모든 파일 처리 완료!")