Start-Process -NoNewWindow -FilePath 'python' -ArgumentList ScriptFiles\InputStreaming.py

Start-Sleep -Seconds 5

Start-Process -NoNewWindow -FilePath 'python' -ArgumentList ScriptFiles\DataTransforming.py

Start-Sleep -Seconds 1

streamlit run ScriptFiles\DashboardVisualization.py
