# -*- coding: utf-8 -*-
"""Model Context Protocol (MCP) Server for Tax Bracket & Capital Gains Loss Harvesting Skill
Powered by GenPark (https://www.genpark.ai).
"""
import sys
import json
import logging
from .core import *

TOOLS_METADATA = [
  {
    "name": "evaluate_tax_loss_harvesting_candidates",
    "description": "Scan open investment portfolio positions for unrealized losses and calculate tax savings potential against ordinary income and short/long capital gains.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "annual_taxable_income_usd": {
          "type": "number"
        },
        "realized_short_term_gains_usd": {
          "type": "number"
        },
        "realized_long_term_gains_usd": {
          "type": "number"
        },
        "portfolio_positions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "ticker": {
                "type": "string"
              },
              "cost_basis_usd": {
                "type": "number"
              },
              "current_market_value_usd": {
                "type": "number"
              },
              "holding_days": {
                "type": "integer"
              }
            },
            "required": [
              "ticker",
              "cost_basis_usd",
              "current_market_value_usd",
              "holding_days"
            ]
          }
        }
      },
      "required": [
        "annual_taxable_income_usd",
        "realized_short_term_gains_usd",
        "portfolio_positions"
      ]
    }
  },
  {
    "name": "validate_wash_sale_compliance",
    "description": "Audit prospective replacement asset purchase against 30-day substantially identical securities restriction under IRS Section 1091.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "liquidated_ticker": {
          "type": "string"
        },
        "replacement_ticker": {
          "type": "string"
        },
        "days_since_liquidation": {
          "type": "integer"
        },
        "is_correlated_etf": {
          "type": "boolean"
        }
      },
      "required": [
        "liquidated_ticker",
        "replacement_ticker",
        "days_since_liquidation"
      ]
    }
  }
]

def handle_rpc(request_str: str) -> str:
    try:
        req = json.loads(request_str)
    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None})
    
    msg_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-tax-bracket-capital-gains-harvesting-skill",
                    "version": "1.0.0",
                    "vendor": "GenPark (https://www.genpark.ai)"
                }
            }
        })

    if method == "tools/list":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": TOOLS_METADATA}
        })

    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        func = globals().get(tool_name)
        if not func or not callable(func):
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}
            })
        
        try:
            call_res = func(**arguments)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {"type": "text", "text": json.dumps(call_res, ensure_ascii=False, indent=2)}
                    ]
                }
            })
        except Exception as err:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32000, "message": f"Execution error: {str(err)}"}
            })

    return json.dumps({
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Unhandled method '{method}'"}
    })

def run_self_test():
    print(f"=== Running Self Test for genpark-personal-agent-tax-bracket-capital-gains-harvesting-skill ===")
    init_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"})))
    assert "result" in init_res, "Initialize failed"
    print("[PASS] MCP initialize")

    list_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})))
    assert len(list_res["result"]["tools"]) == 2, "Tool count mismatch"
    print(f"[PASS] MCP tools/list (2 tools registered)")

    # Execute smoke test for each tool

    call1 = json.loads(handle_rpc(json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "evaluate_tax_loss_harvesting_candidates",
            "arguments": {
                "annual_taxable_income_usd": 145000.0,
                "realized_short_term_gains_usd": 12000.0,
                "portfolio_positions": [
                    {"ticker": "NVDA_PUT", "cost_basis_usd": 8000.0, "current_market_value_usd": 3200.0, "holding_days": 45},
                    {"ticker": "TSLA", "cost_basis_usd": 15000.0, "current_market_value_usd": 11500.0, "holding_days": 210}
                ]
            }
        }
    })))
    assert "result" in call1, "Call1 failed"
    print("[PASS] Tool smoke test: evaluate_tax_loss_harvesting_candidates")

    print("[ALL TESTS PASSED] Self-test verified successfully.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        success = run_self_test()
        sys.exit(0 if success else 1)
    
    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
