# Hong Kong Monthly Temperature Matrix (Last 10 Years)

This project visualizes Hong Kong temperature data using a matrix layout:

- X-axis: Year  
- Y-axis: Month  
- Background color encodes monthly temperature  
- Daily sparklines (green = max, blue = min)  
- Hover format:  
  Date YYYY-MM-DD, max: xxx℃, min: xxx℃  
- Unified color legend  
- MAX / MIN toggle button

The output figure is in the 'output' folder.

---

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

## AI Log
Conversation link:
https://chatgpt.com/share/699ba5e8-fe80-800b-bac2-d4caf093d23c


## AI Reflection
AI was used to:

1. Identify an appropriate library (Plotly) for interactive matrix visualization

2. Provide guidance on subplot layout and heatmap usage

3. Helps me debug axes issue

The AI assisted primarily in debugging and implementation refinement.
All final design decisions and integration were completed manually.
