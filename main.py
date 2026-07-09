# .github/workflows/build.yml
# Kodingizni to'g'ri papkaga joylash uchun ushbu skriptni ishga tushiring
import os

path = ".github/workflows"
os.makedirs(path, exist_ok=True)

workflow_code = """name: APK Yigish Bot

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-state: '3.10'
    - name: Install Buildozer
      run: |
        pip install --user --upgrade buildozer build cython virtualenv
    - name: Build APK with Buildozer
      run: |
        buildozer android debug
    - name: Upload APK Artifact
      uses: actions/upload-artifact@v3
      with:
        name: package
        path: bin/*.apk
"""

with open(f"{path}/build.yml", "w") as f:
    f.write(workflow_code)

print("Robot muvaffaqiyatli to'g'ri papkaga joylandi!")
