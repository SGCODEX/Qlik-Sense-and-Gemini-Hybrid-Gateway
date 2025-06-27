import asyncio
import websockets
import json
import os

# Full path to your Qlik app file
QLIK_APP_PATH = os.path.abspath("C:/Users/Admin/Documents/Qlik/Sense/Apps/SalesAppFromQVD.qvf").replace("\\", "/")

async def fetch_data_from_qlik_ws():
    print("Connecting to Qlik WebSocket...")
    ws_url = "ws://localhost:4848/app/"

    async with websockets.connect(ws_url) as ws:
        print("✅ Connected to Qlik WebSocket.")

        app_filename = os.path.basename(QLIK_APP_PATH)
        print("📄 Attempting to open app file:", app_filename)

        # STEP 1: Open the Qlik app
        await ws.send(json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "handle": -1,
            "method": "OpenDoc",
            "params": {"qDocName": app_filename}
        }))

        while True:
            raw_msg = await ws.recv()
            msg = json.loads(raw_msg)
            if msg.get("id") == 1:
                open_doc_response = msg
                break

        if "result" not in open_doc_response:
            raise Exception(f"❌ OpenDoc failed: {open_doc_response.get('error')}")

        app_handle = open_doc_response["result"]["qReturn"]["qHandle"]
        print(f"✅ App Opened! Handle = {app_handle}")

        # STEP 2: Get App Layout (optional)
        await ws.send(json.dumps({
            "jsonrpc": "2.0",
            "id": 2,
            "handle": app_handle,
            "method": "GetAppLayout",
            "params": {}
        }))
        layout_response = json.loads(await ws.recv())
        print("✅ App Layout:", layout_response)

        # STEP 3: Create HyperCube with more fields
        await ws.send(json.dumps({
            "jsonrpc": "2.0",
            "id": 3,
            "handle": app_handle,
            "method": "CreateSessionObject",
            "params": {
                "qProp": {
                    "qInfo": {"qType": "Chart"},
                    "qHyperCubeDef": {
                        "qDimensions": [
                            {"qDef": {"qFieldDefs": ["Product"]}},
                            {"qDef": {"qFieldDefs": ["Region"]}},
                            {"qDef": {"qFieldDefs": ["Date.autoCalendar.Month"]}}
                        ],
                        "qMeasures": [
                            {"qDef": {"qDef": "Sum(Sales)"}},
                            {"qDef": {"qDef": "Sum([Units Sold])"}}
                        ],
                        "qInitialDataFetch": [{"qTop": 0, "qLeft": 0, "qHeight": 100, "qWidth": 5}]
                    }
                }
            }
        }))

        create_obj_response = json.loads(await ws.recv())
        if "result" not in create_obj_response:
            raise Exception(f"❌ CreateSessionObject failed: {create_obj_response.get('error')}")

        chart_handle = create_obj_response["result"]["qReturn"]["qHandle"]

        # STEP 4: Fetch HyperCube Data
        await ws.send(json.dumps({
            "jsonrpc": "2.0",
            "id": 4,
            "handle": chart_handle,
            "method": "GetHyperCubeData",
            "params": {
                "qPath": "/qHyperCubeDef",
                "qPages": [{"qTop": 0, "qLeft": 0, "qHeight": 100, "qWidth": 5}]
            }
        }))

        hypercube = json.loads(await ws.recv())
        print("📊 Hypercube response:", hypercube)

        # STEP 5: Parse Data
        pages = hypercube.get("result", {}).get("qDataPages", [])
        if not pages:
            raise Exception("❌ No qDataPages found.")
        matrix = pages[0].get("qMatrix", [])
        if not matrix:
            raise Exception("❌ qMatrix is empty.")

        data = []
        for row in matrix:
            product = row[0]['qText']
            region = row[1]['qText']
            month = row[2]['qText']
            sales = row[3]['qNum']
            units = row[4]['qNum']
            data.append({
                'Product': product,
                'Region': region,
                'Month': month,
                'Sales': sales,
                'Units Sold': units
            })

        return data

# Sync wrapper
def get_qlik_data():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(fetch_data_from_qlik_ws())
    else:
        return asyncio.run(fetch_data_from_qlik_ws())
