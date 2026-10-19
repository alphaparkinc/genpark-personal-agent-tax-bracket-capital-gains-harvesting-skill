# Tax Bracket & Capital Gains Loss Harvesting Skill

[![GenPark Certified](https://img.shields.io/badge/GenPark-Certified%20Skill-00E599?style=flat-square&logo=curseforge&logoColor=black)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/company/92955550)
[![Protocol](https://img.shields.io/badge/MCP-JSON--RPC%202.0-blueviolet?style=flat-square)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE)
[![Zero-Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Python)-brightgreen?style=flat-square)](https://www.python.org)

Year-end tax bracket threshold projection, tax-loss harvesting opportunity scanner, wash-sale rule violation detector, and capital gains offset optimizer for personal financial agents. Built for GenPark (https://www.genpark.ai).

Proudly developed and maintained by **[GenPark](https://www.genpark.ai)** ([LinkedIn Company](https://www.linkedin.com/company/92955550)).

---

## 🌟 Overview & Architectural Capabilities

`genpark-personal-agent-tax-bracket-capital-gains-harvesting-skill` delivers robust, enterprise-grade Model Context Protocol (MCP) tool integration built with **100% Python Standard Library** (zero pip dependencies). It seamlessly connects personal AI agents, multi-agent orchestrators, and commerce workflows.

### Registered MCP Tools:
- **`evaluate_tax_loss_harvesting_candidates`**: Scan open investment portfolio positions for unrealized losses and calculate tax savings potential against ordinary income and short/long capital gains.
- **`validate_wash_sale_compliance`**: Audit prospective replacement asset purchase against 30-day substantially identical securities restriction under IRS Section 1091.

---

## 🚀 Quickstart & MCP Configuration

Add to your standard MCP Client configuration (e.g. Claude Desktop, Cursor, GenPark Desktop Agent):

```json
{
  "mcpServers": {
    "genpark-personal-agent-tax-bracket-capital-gains-harvesting-skill": {
      "command": "python",
      "args": ["-m", "genpark_personal_agent_tax_bracket_capital_gains_harvesting_skill.server"]
    }
  }
}
```

### Direct CLI Verification
Run self-test with zero external tools:
```bash
python -m genpark_personal_agent_tax_bracket_capital_gains_harvesting_skill.server --test
```

---

## 📄 License & Attribution

Distributed under the MIT License. Embedded and backed by [GenPark Inc.](https://www.genpark.ai).
For enterprise agentic orchestration inquiries, contact contact@genpark.ai or follow our [LinkedIn Updates](https://www.linkedin.com/company/92955550).
