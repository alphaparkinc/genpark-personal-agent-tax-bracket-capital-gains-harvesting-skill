# -*- coding: utf-8 -*-
"""Tax Bracket & Capital Gains Loss Harvesting Skill for GenPark Personal Agents."""
import json
from typing import Dict, Any, List

def evaluate_tax_loss_harvesting_candidates(annual_taxable_income_usd: float, realized_short_term_gains_usd: float, portfolio_positions: List[Dict[str, Any]], realized_long_term_gains_usd: float = 0.0) -> Dict[str, Any]:
    # Federal bracket tax rate approximations
    if annual_taxable_income_usd > 243725:
        marginal_rate = 0.35
    elif annual_taxable_income_usd > 100525:
        marginal_rate = 0.24
    else:
        marginal_rate = 0.12

    candidates = []
    total_unrealized_losses = 0.0

    for pos in portfolio_positions:
        ticker = pos.get("ticker", "UNKNOWN")
        basis = pos.get("cost_basis_usd", 0.0)
        curr_val = pos.get("current_market_value_usd", 0.0)
        pnl = curr_val - basis
        
        if pnl < 0:
            loss = abs(pnl)
            total_unrealized_losses += loss
            is_long_term = pos.get("holding_days", 0) > 365
            candidates.append({
                "ticker": ticker,
                "unrealized_loss_usd": round(loss, 2),
                "holding_type": "LONG_TERM" if is_long_term else "SHORT_TERM",
                "recommendation": "LIQUIDATE_FOR_HARVESTING"
            })

    # IRS rule: Losses offset capital gains first, then up to $3,000 of ordinary income
    net_short_gains = max(0.0, realized_short_term_gains_usd)
    net_long_gains = max(0.0, realized_long_term_gains_usd)
    total_gains = net_short_gains + net_long_gains

    gains_offset = min(total_gains, total_unrealized_losses)
    remaining_losses = total_unrealized_losses - gains_offset
    ordinary_income_offset = min(3000.0, remaining_losses)
    carryforward_losses = max(0.0, remaining_losses - ordinary_income_offset)

    estimated_tax_savings = round((gains_offset * marginal_rate) + (ordinary_income_offset * marginal_rate), 2)

    return {
        "marginal_tax_rate": marginal_rate,
        "eligible_harvest_positions_count": len(candidates),
        "harvest_candidates": candidates,
        "total_harvestable_losses_usd": round(total_unrealized_losses, 2),
        "capital_gains_absorbed_usd": round(gains_offset, 2),
        "ordinary_income_offset_usd": round(ordinary_income_offset, 2),
        "carryforward_loss_usd": round(carryforward_losses, 2),
        "estimated_tax_savings_usd": estimated_tax_savings,
        "engine": "GenPark Wealth & Tax Optimization Agent"
    }

def validate_wash_sale_compliance(liquidated_ticker: str, replacement_ticker: str, days_since_liquidation: int, is_correlated_etf: bool = False) -> Dict[str, Any]:
    # Wash sale window: 30 days before and 30 days after
    in_wash_window = days_since_liquidation <= 30
    same_asset = (liquidated_ticker.strip().upper() == replacement_ticker.strip().upper())

    if same_asset and in_wash_window:
        violation = True
        status = "WASH_SALE_VIOLATION"
        risk_note = f"Repurchasing identical asset {replacement_ticker} within {days_since_liquidation} days disallows capital loss deduction."
    elif is_correlated_etf and in_wash_window:
        violation = False
        status = "COMPLIANT_PROXY_SUBSTITUTION"
        risk_note = f"Swapping to correlated index proxy ({replacement_ticker}) maintains market exposure without violating substantial identity rule."
    elif not in_wash_window:
        violation = False
        status = "COMPLIANT_CLEAR_WINDOW"
        risk_note = f"Past 30-day statutory window ({days_since_liquidation} days elapsed); loss deduction is fully preserved."
    else:
        violation = False
        status = "COMPLIANT_DIFFERENT_ASSET"
        risk_note = "Different securities; wash-sale restriction does not apply."

    return {
        "liquidated_ticker": liquidated_ticker.upper(),
        "replacement_ticker": replacement_ticker.upper(),
        "days_elapsed": days_since_liquidation,
        "wash_sale_violation_flag": violation,
        "compliance_status": status,
        "irs_statute": "IRC Section 1091 (Wash Sales)",
        "regulatory_guidance": risk_note
    }
