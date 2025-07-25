DASHBOARD_STYLE = """
    <style>
        .main-header {
            text-align: center;
            padding: 2rem 0;
            color: #1f4e79;  /* Hiya blue */
            margin-bottom: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .logo-image {
            max-width: 300px;  /* Increased from 180px */
            height: auto;
            margin-bottom: 2rem;  /* Increased from 1.5rem */
        }

        .main-header h1 {
            font-size: 2.2rem;
            font-weight: 600;
            margin: 0.5rem 0;
            color: #000000;  /* Changed to black */
        }

        .metric-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .metric-card:hover {
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }

        .insight-box {
            background: #f8fafc;
            border-left: 4px solid #1f4e79;  /* Hiya blue accent */
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 0 8px 8px 0;
        }

        .insight-box h3 {
            color: #1f4e79;  /* Hiya blue */
            margin: 0 0 0.5rem 0;
        }

        .insight-box p {
            color: #4b5563;
            margin: 0;
            line-height: 1.5;
        }
    </style>
"""