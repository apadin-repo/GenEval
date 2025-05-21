
# style class
class Style:

    TABLE_CSS = """
        table {
        border-collapse: collapse;
        width: 100%;
        }
        th, td {
        border: 1px solid #444;
        padding: 8px;
        text-align: left;
        }
        th {
        background-color: #f2f2f2;
        }
    """
    
    CSS = """
        #output-container {
            border-radius: 8px;
            border: 1px solid #d1d5db;
            padding: 8px 16px;
        }
        div {
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
        }
        .green-button {
            background-color: #22c55e !important;  /* Tailwind green-500 */
            color: white !important;
            font-weight: bold;
            border-radius: 6px;
            padding: 8px 16px;
        }
        .green-button:hover {
            background-color: #16a34a !important;  /* Tailwind green-600 */
        }
        #output-container {
            border-radius: 8px !important;
            border: 1px solid #d1d5db !important;
            padding: 8px 16px !important;
            margin-bottom: 12px !important;
            max-height: 900px;
            overflow-y: auto;
        }
        #upload-container {
            border-radius: 8px !important;
            border: 1px dashed #d1d5db !important;
            padding: 8px 16px !important;
            margin-bottom: 12px !important;
        }
    """

Style = Style()