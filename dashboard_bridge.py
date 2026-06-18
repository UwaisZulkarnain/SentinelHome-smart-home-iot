#!/usr/bin/env python3
"""
🔌 Serial → WebSocket Bridge
Forwards your XIAO ESP32S3 serial output to a WebSocket server.
The web dashboard (dashboard_web.html) connects to this.

Usage:
  1. python dashboard_bridge.py COM3
  2. Open dashboard_web.html in browser
  3. Click "Connect" (defaults to ws://localhost:8765)

Requires: pip install pyserial websockets
"""

import asyncio
import serial
import serial.tools.list_ports
import sys
import json
import re
from datetime import datetime

import websockets

# ─── CONFIG ───
WS_PORT = 8765
BAUD = 115200

clients = set()

async def broadcast(data):
    if clients:
        msg = json.dumps(data)
        await asyncio.gather(*[c.send(msg) for c in clients], return_exceptions=True)

async def handle_client(ws, path):
    clients.add(ws)
    print(f"🌐 Dashboard connected ({len(clients)} total)")
    try:
        await ws.wait_closed()
    finally:
        clients.discard(ws)
        print(f"🌐 Dashboard disconnected ({len(clients)} remaining)")

def parse_serial_line(line):
    """Parse JSON: prefix or text format"""
    line = line.strip()
    if line.startswith("JSON:"):
        try:
            return json.loads(line[5:])
        except:
            pass
    # Text fallback
    result = {}
    if 'Temperature:' in line:
        m = re.search(r'Temperature:\s*([\d.]+)', line)
        if m: result['t'] = float(m.group(1))
    if 'Humidity:' in line:
        m = re.search(r'Humidity:\s*([\d.]+)', line)
        if m: result['h'] = float(m.group(1))
    if 'Motion:' in line:
        result['m'] = 1 if 'YES' in line else 0
    if 'Gas:' in line:
        result['g'] = 1 if 'DETECTED' in line else 0
    if 'Alarm:' in line:
        result['a'] = 1 if 'ACTIVE' in line else 0
    return result if result else None

async def serial_reader(port):
    loop = asyncio.get_event_loop()
    try:
        ser = serial.Serial(port, BAUD, timeout=0.1)
        print(f"✅ Serial connected to {port} @ {BAUD}")
    except Exception as e:
        print(f"❌ Failed to open serial: {e}")
        return

    while True:
        try:
            line = await loop.run_in_executor(None, ser.readline)
            if line:
                text = line.decode('utf-8', errors='ignore').strip()
                if text:
                    data = parse_serial_line(text)
                    if data:
                        data['_ts'] = datetime.now().isoformat()
                        print(f"📡 {text[:60]}")
                        await broadcast(data)
        except Exception as e:
            print(f"⚠️ Serial error: {e}")
            await asyncio.sleep(1)

async def main():
    if len(sys.argv) < 2:
        print("Usage: python dashboard_bridge.py <COM_PORT>")
        print("\nAvailable ports:")
        for p in serial.tools.list_ports.comports():
            print(f"  {p.device} - {p.description}")
        sys.exit(1)

    port = sys.argv[1]

    ws_server = await websockets.serve(handle_client, "localhost", WS_PORT)
    print(f"🚀 WebSocket server running on ws://localhost:{WS_PORT}")
    print(f"📟 Reading serial from {port}...")
    print("\nOpen dashboard_web.html in your browser and click Connect\n")

    await serial_reader(port)

if __name__ == "__main__":
    asyncio.run(main())
