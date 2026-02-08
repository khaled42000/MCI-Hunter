name: Update MCI Configs

on:
  schedule:
    - cron: '0 */1 * * *' # اجرا هر 4 ساعت
  workflow_dispatch: # امکان اجرای دستی

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install Dependencies
        run: |
          pip install requests

      - name: Run Harvester Script
        run: python main.py

      - name: Commit and Push
        run: |
          git config --global user.name "GitHub Action"
          git config --global user.email "action@github.com"
          git add sub.txt sub_b64.txt
          git commit -m "Auto Update Configs" || echo "No changes to commit"
          git push
