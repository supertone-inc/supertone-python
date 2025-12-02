#!/bin/bash

# Speakeasy SDK 생성을 단계별로 실행하는 스크립트
set -e

# 인자 파싱
INSTALL_UV_AUTO=false
START_STEP="lint"

# 인자 처리
while [[ $# -gt 0 ]]; do
    case $1 in
        --auto-install-uv)
            INSTALL_UV_AUTO=true
            shift
            ;;
        *)
            START_STEP=$1
            shift
            ;;
    esac
done

# 단계 순서 정의
STEPS=("lint" "generate" "fix" "install" "typecheck" "lint-code" "docs" "build" "publish")

# 시작 단계의 인덱스 찾기
START_INDEX=-1
for i in "${!STEPS[@]}"; do
    if [[ "${STEPS[$i]}" == "$START_STEP" ]]; then
        START_INDEX=$i
        break
    fi
done

if [ $START_INDEX -eq -1 ]; then
    echo "❌ Invalid step: $START_STEP"
    echo "Available steps: ${STEPS[*]}"
    exit 1
fi

echo "Starting from step: $START_STEP"

# uv 자동 설치
if ! command -v uv &> /dev/null; then
    echo ""
    echo "⚠️  uv가 설치되지 않았습니다."
    
    SHOULD_INSTALL=false
    
    if [ "$INSTALL_UV_AUTO" = true ]; then
        echo "자동 설치 모드로 uv를 설치합니다..."
        SHOULD_INSTALL=true
    else
        echo "더 빠른 패키지 관리를 위해 uv를 설치하시겠습니까?"
        echo ""
        read -p "uv를 설치하시겠습니까? (Y/n): " -n 1 -r
        echo
        
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            SHOULD_INSTALL=true
        fi
    fi
    
    if [ "$SHOULD_INSTALL" = false ]; then
        echo "uv 설치를 건너뛰고 pip을 사용합니다."
    else
        echo "uv 설치 중..."
        
        # 운영체제별 설치 방법
        if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # macOS 또는 Linux
            if command -v curl &> /dev/null; then
                curl -LsSf https://astral.sh/uv/install.sh | sh
                
                # PATH에 추가 (현재 세션에서만)
                export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"
                
                # 설치 확인
                if command -v uv &> /dev/null; then
                    echo "✅ uv 설치 완료!"
                    echo "참고: uv를 영구적으로 사용하려면 다음을 ~/.bashrc 또는 ~/.zshrc에 추가하세요:"
                    echo "export PATH=\"\$HOME/.cargo/bin:\$PATH\""
                else
                    echo "❌ uv 설치 실패. pip을 사용합니다."
                fi
            else
                echo "curl이 없습니다. pip으로 uv를 설치합니다..."
                pip install uv
                
                if command -v uv &> /dev/null; then
                    echo "✅ uv 설치 완료!"
                else
                    echo "❌ uv 설치 실패. pip을 사용합니다."
                fi
            fi
        else
            # Windows 또는 기타
            echo "Windows에서는 pip으로 uv를 설치합니다..."
            pip install uv
            
            if command -v uv &> /dev/null; then
                echo "✅ uv 설치 완료!"
            else
                echo "❌ uv 설치 실패. pip을 사용합니다."
            fi
        fi
    fi
    echo ""
fi

# lint: OpenAPI 스펙 검증
if [ $START_INDEX -le 0 ]; then
    echo "=== OpenAPI 스펙 검증 ==="
    speakeasy lint openapi openapi.json
fi

# generate: 완전한 SDK 및 Docs 재생성
if [ $START_INDEX -le 1 ]; then
    echo -e "\n=== 완전한 SDK 및 문서 재생성 ==="
    
    # 1. 기존 생성 파일들 백업
    BACKUP_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    echo "🔄 기존 파일들 백업 중..."
    
    # docs 폴더 백업
    if [ -d "docs" ]; then
        echo "  📁 docs -> docs_backup_$BACKUP_TIMESTAMP"
        mv docs docs_backup_$BACKUP_TIMESTAMP
    fi
    
    # README.md 백업
    if [ -f "README.md" ]; then
        echo "  📄 README.md -> README_backup_$BACKUP_TIMESTAMP.md"
        cp README.md README_backup_$BACKUP_TIMESTAMP.md
    fi
    
    # USAGE.md 백업
    if [ -f "USAGE.md" ]; then
        echo "  📄 USAGE.md -> USAGE_backup_$BACKUP_TIMESTAMP.md"
        cp USAGE.md USAGE_backup_$BACKUP_TIMESTAMP.md
    fi
    
    # 2. 완전한 SDK 재생성
    echo "🚀 완전한 SDK 재생성 중..."
    echo "  📋 Using schema: openapi.json"
    echo "  🎯 Target language: Python"
    echo "  📦 Output directory: ."
    
    speakeasy generate sdk \
        --lang python \
        --schema openapi.json \
        --out . \
        --auto-yes
    
    # 3. 생성 결과 검증
    if [ $? -eq 0 ]; then
        echo "✅ SDK 재생성 완료!"
        
        # 생성된 주요 파일들 확인
        echo "📊 생성 결과 요약:"
        [ -f README.md ] && echo "  ✅ README.md ($(wc -l < README.md) lines)" || echo "  ❌ README.md"
        [ -f USAGE.md ] && echo "  ✅ USAGE.md ($(wc -l < USAGE.md) lines)" || echo "  ❌ USAGE.md"
        [ -d docs ] && echo "  ✅ docs/ ($(find docs -name "*.md" | wc -l | tr -d ' ') markdown files)" || echo "  ❌ docs/"
        [ -d src/supertone ] && echo "  ✅ src/supertone/ ($(find src/supertone -name "*.py" | wc -l | tr -d ' ') Python files)" || echo "  ❌ src/supertone/"
        
        # Summary 섹션 확인 (가장 중요!)
        if [ -f README.md ]; then
            echo "📝 README.md Summary 확인:"
            if grep -A5 "<!-- Start Summary \[summary\] -->" README.md | grep -q "Supertone\|API"; then
                echo "  ✅ Summary 내용이 올바르게 생성됨"
                grep -A3 "## Summary" README.md | tail -2
            else
                echo "  ⚠️  Summary가 비어있거나 불완전함"
            fi
        fi
        
    else
        echo "❌ SDK 생성 실패!"
        echo "💡 백업된 파일들을 복원하시겠습니까?"
        echo "  docs_backup_$BACKUP_TIMESTAMP -> docs"
        echo "  README_backup_$BACKUP_TIMESTAMP.md -> README.md"
        echo "  USAGE_backup_$BACKUP_TIMESTAMP.md -> USAGE.md"
        exit 1
    fi
fi

# fix: Python 버전 수정
if [ $START_INDEX -le 2 ]; then
    echo -e "\n=== Python 버전 수정 ==="
    ./fix-python-version.sh
fi

# install: 의존성 설치
if [ $START_INDEX -le 3 ]; then
    echo -e "\n=== 의존성 설치 ==="
    
    # Python 3.12 환경 확인 및 설정
    PYTHON_CMD="python"
    
    # pyenv에서 Python 3.12 찾기 및 설정
    if command -v pyenv &> /dev/null; then
        AVAILABLE_312=$(pyenv versions --bare | grep -E '^3\.12\.' | head -1)
        if [ -n "$AVAILABLE_312" ]; then
            echo "Using pyenv Python $AVAILABLE_312"
            pyenv local $AVAILABLE_312
            PYTHON_CMD="python"
        else
            echo "❌ Python 3.12 not found in pyenv. Please install: pyenv install 3.12.6"
            exit 1
        fi
    else
        # pyenv가 없으면 python3.12 직접 찾기
        if command -v python3.12 &> /dev/null; then
            PYTHON_CMD="python3.12"
        else
            echo "❌ Python 3.12 not found. Please install Python 3.12 or pyenv"
            exit 1
        fi
    fi
    
    if command -v uv &> /dev/null; then
        echo "Installing dependencies with uv..."
        uv sync --python $PYTHON_CMD
    else
        echo "Installing dependencies with pip..."
        $PYTHON_CMD -m pip install -e .
    fi
fi

# typecheck: 타입 체크
if [ $START_INDEX -le 4 ]; then
    echo -e "\n=== 타입 체크 ==="
    
    # uv PATH 추가 (설치 후)
    export PATH="$HOME/.local/bin:$PATH"
    
    # 가상환경 활성화 (uv 또는 venv)
    if command -v uv &> /dev/null && [ -f ".venv/bin/activate" ]; then
        echo "Activating virtual environment..."
        source .venv/bin/activate
    elif [ -f ".venv/bin/activate" ]; then
        echo "Activating virtual environment..."
        source .venv/bin/activate
    fi
    
    # pyright 설치 확인 및 자동 설치 (가상환경에서 강제 설치)
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "Installing pyright in virtual environment..."
        pip install pyright
    else
        # 시스템에서 pyright 확인 및 설치
        if ! command -v pyright &> /dev/null; then
            echo "⚠️  pyright not found! Installing..."
            if command -v npm &> /dev/null; then
                echo "Installing pyright with npm..."
                npm install -g pyright
            else
                echo "Installing pyright with pip..."
                $PYTHON_CMD -m pip install pyright
            fi
        fi
    fi
    
    echo "Running pyright type check..."
    
    if pyright src/supertone/; then
        echo "✅ Type check passed successfully!"
    else
        echo "❌ Type check failed!"
        echo "타입 에러를 수정한 후 다시 실행하세요."
        exit 1
    fi
fi

# lint-code: 린트 체크
if [ $START_INDEX -le 5 ]; then
    echo -e "\n=== 린트 체크 (optional) ==="
    if command -v pylint &> /dev/null; then
        echo "Running pylint..."
        pylint src/supertone/ || echo "Lint check completed with warnings"
    else
        echo "pylint not found, skipping lint check"
    fi
fi

# docs: 문서 최종 검증 및 완성
if [ $START_INDEX -le 6 ]; then
    echo -e "\n=== 문서 최종 검증 및 완성 ==="
    
    # 1. Production warning 제거
    if [ -f README.md ] && grep -q "This SDK is not yet ready for production use" README.md; then
        echo "🔧 Production warning 제거 중..."
        sed -i '' '/> \[!IMPORTANT\]/,/> publishing to a package manager\./d' README.md
        echo "  ✅ Production warning 제거됨"
    fi
    
    # 2. 패키지 정보 확인
    PACKAGE_NAME=$(grep '^name = ' pyproject.toml | sed 's/name = "\(.*\)"/\1/')
    PACKAGE_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
    echo "📦 Package: $PACKAGE_NAME v$PACKAGE_VERSION"
    
    # 3. 문서 구조 상세 분석
    echo "📚 완전한 문서 구조 분석:"
    
    # README.md 분석
    if [ -f README.md ]; then
        echo "  📄 README.md:"
        echo "    - 총 $(wc -l < README.md | tr -d ' ') lines"
        echo "    - Table of Contents: $(grep -c "## " README.md) sections"
        echo "    - Code examples: $(grep -c '```' README.md) blocks"
    fi
    
    # USAGE.md 분석  
    if [ -f USAGE.md ]; then
        echo "  📄 USAGE.md:"
        echo "    - 총 $(wc -l < USAGE.md | tr -d ' ') lines"
        echo "    - Usage examples: $(grep -c '## ' USAGE.md) sections"
    fi
    
    # docs 폴더 구조 분석
    if [ -d docs ]; then
        echo "  📁 docs/ 구조:"
        echo "    - 총 $(find docs -name "*.md" | wc -l | tr -d ' ') markdown files"
        echo "    - models/: $(find docs/models -name "*.md" 2>/dev/null | wc -l | tr -d ' ') files"
        echo "    - errors/: $(find docs/errors -name "*.md" 2>/dev/null | wc -l | tr -d ' ') files"
        echo "    - sdks/: $(find docs/sdks -name "*.md" 2>/dev/null | wc -l | tr -d ' ') files"
        
        # 주요 문서 파일들 나열
        echo "    📋 주요 문서들:"
        find docs -maxdepth 2 -name "*.md" | head -5 | sed 's/^/      /'
        if [ $(find docs -name "*.md" | wc -l) -gt 5 ]; then
            echo "      ... and $(( $(find docs -name "*.md" | wc -l) - 5 )) more files"
        fi
    fi
    
    # 4. GitHub Pages 준비
    echo "🌐 GitHub Pages 준비:"
    if [ ! -f docs/index.md ]; then
        echo "  📝 docs/index.md 생성 중..."
        cp README.md docs/index.md
        echo "  ✅ docs/index.md 생성됨"
    else
        echo "  ✅ docs/index.md 이미 존재"
    fi
    
    # 5. 최종 품질 검증
    echo "🔍 문서 품질 최종 검증:"
    
    # Summary 검증
    if [ -f README.md ]; then
        if grep -A5 "<!-- Start Summary \[summary\] -->" README.md | grep -q "Supertone\|Text-to-Speech\|API"; then
            echo "  ✅ Summary 내용 완벽"
        else
            echo "  ⚠️  Summary 내용 확인 필요"
        fi
    fi
    
    # 링크 검증 (간단한)
    if [ -f README.md ]; then
        BROKEN_LINKS=$(grep -o '\[.*\](.*\.md)' README.md | sed 's/.*](//' | sed 's/)//' | while read link; do
            if [ ! -f "$link" ]; then
                echo "$link"
            fi
        done | wc -l)
        
        if [ "$BROKEN_LINKS" -eq 0 ]; then
            echo "  ✅ 내부 링크 검증 통과"
        else
            echo "  ⚠️  $BROKEN_LINKS 개의 깨진 링크 발견"
        fi
    fi
    
    # 6. 성공 메시지 및 요약
    echo ""
    echo "🎉 완전한 문서 재생성 완료!"
    echo "📊 최종 결과:"
    echo "  - 백업: docs_backup_$(date +%Y%m%d)_* 폴더들"
    echo "  - README.md: $([ -f README.md ] && echo "✅ 생성됨" || echo "❌ 실패")"
    echo "  - USAGE.md: $([ -f USAGE.md ] && echo "✅ 생성됨" || echo "❌ 실패")"  
    echo "  - docs/: $([ -d docs ] && echo "✅ $(find docs -name "*.md" | wc -l | tr -d ' ') files" || echo "❌ 실패")"
    echo "  - GitHub Pages: $([ -f docs/index.md ] && echo "✅ 준비완료" || echo "❌ 미완성")"
    
    echo ""
    echo "🚀 이제 다음과 같이 확인하세요:"
    echo "  1. README.md 내용 확인"
    echo "  2. docs/ 폴더 구조 확인"  
    echo "  3. 필요시 GitHub Pages 설정"
    echo "  4. 백업 파일들은 만족스러우면 삭제 가능"
fi

# build: 패키지 빌드
if [ $START_INDEX -le 7 ]; then
    echo -e "\n=== 패키지 빌드 ==="
    
    # 기존 dist 폴더 정리
    if [ -d "dist" ]; then
        echo "Cleaning up existing dist directory..."
        rm -rf dist/
    fi
    
    # uv 우선 사용, 없으면 python -m build 사용
    if command -v uv &> /dev/null; then
        echo "Building package with uv..."
        uv build
    else
        echo "uv not found, using python -m build..."
        
        # build 모듈 확인 및 설치
        if ! python -c "import build" &> /dev/null; then
            echo "Installing build module..."
            pip install build
        fi
        
        echo "Building package..."
        python -m build
    fi
    
    if [ $? -eq 0 ]; then
        echo "✅ Package built successfully!"
        echo "Built files:"
        ls -la dist/
    else
        echo "❌ Package build failed!"
        exit 1
    fi
fi

# publish: PyPI 배포
if [ $START_INDEX -le 8 ]; then
    echo -e "\n=== PyPI 배포 (선택사항) ==="
    
    # dist 폴더 확인
    if [ ! -d "dist" ] || [ -z "$(ls -A dist/)" ]; then
        echo "❌ No built packages found in dist/ directory"
        echo "Run 'build' step first"
        exit 1
    fi
    
    echo "Available packages in dist/:"
    ls -la dist/
    
    echo ""
    echo "⚠️  PyPI 배포를 진행하시겠습니까?"
    echo "배포 전에 다음을 확인하세요:"
    echo "1. PyPI 계정과 API 토큰이 설정되어 있는지"
    echo "2. 패키지 이름과 버전이 올바른지"
    echo "3. 테스트가 완료되었는지"
    echo ""
    read -p "계속 진행하시겠습니까? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # uv 우선 사용, 없으면 twine 사용
        if command -v uv &> /dev/null; then
            echo "Uploading to PyPI with uv..."
            if [ -n "$PYPI_TOKEN" ]; then
                uv publish --token $PYPI_TOKEN
            else
                echo "Environment variable PYPI_TOKEN not set."
                echo "Please set your PyPI token: export PYPI_TOKEN=your_token"
                uv publish
            fi
        else
            echo "uv not found, using twine..."
            
            # twine 설치 확인
            if ! command -v twine &> /dev/null; then
                echo "Installing twine..."
                pip install twine
            fi
            
            echo "Uploading to PyPI with twine..."
            twine upload dist/*
        fi
        
        if [ $? -eq 0 ]; then
            echo "✅ Successfully uploaded to PyPI!"
        else
            echo "❌ PyPI upload failed!"
            exit 1
        fi
    else
        echo "PyPI 배포를 건너뛰었습니다."
        if command -v uv &> /dev/null; then
            echo "수동으로 배포하려면: uv publish --token \$PYPI_TOKEN"
        else
            echo "수동으로 배포하려면: twine upload dist/*"
        fi
    fi
fi

echo -e "\n=== 전체 과정 완료! ==="
echo "생성된 패키지:"
if [ -d "dist" ]; then
    ls -la dist/
fi