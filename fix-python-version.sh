#!/bin/bash

# Speakeasy 실행 후 Python 버전을 3.12로 수정하는 스크립트
echo "Fixing Python version in pyproject.toml to >=3.12..."

# pyproject.toml에서 requires-python을 3.12로 변경
sed -i '' 's/requires-python = ">=3\.9\.2"/requires-python = ">=3.12"/g' pyproject.toml

# pyright 설정에 pythonVersion과 exclude 추가
echo "Adding pyright configuration..."

# pyright 섹션이 이미 있는지 확인하고 pythonVersion과 exclude 추가
if grep -q '\[tool\.pyright\]' pyproject.toml; then
    # 기존 pyright 섹션에 pythonVersion 추가 (없는 경우만)
    if ! grep -q 'pythonVersion = "3.12"' pyproject.toml; then
        sed -i '' '/\[tool\.pyright\]/a\
pythonVersion = "3.12"
' pyproject.toml
    fi
    
    # exclude 설정 추가 (없는 경우만)
    if ! grep -q 'exclude = \["src_backup_\*"\]' pyproject.toml; then
        sed -i '' '/\[tool\.pyright\]/a\
exclude = ["src_backup_*"]
' pyproject.toml
    fi
fi

# 변경 결과 확인
if grep -q 'requires-python = ">=3.12"' pyproject.toml; then
    echo "✓ Python version successfully updated to >=3.12"
else
    echo "✗ Failed to update Python version"
    exit 1
fi

if grep -q 'pythonVersion = "3.12"' pyproject.toml; then
    echo "✓ Pyright Python version set to 3.12"
fi

if grep -q 'exclude = \["src_backup_\*"\]' pyproject.toml; then
    echo "✓ Backup folders excluded from pyright"
fi

echo "Done!"