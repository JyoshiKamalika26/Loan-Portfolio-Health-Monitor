from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def generate_pdf(
    total_loans,
    total_loan_value,
    overall_npa_rate,
    avg_recovery,
    health_score,
    low_risk_count,
    medium_risk_count,
    high_risk_count
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    # =================================
    # TITLE
    # =================================

    elements.append(
        Paragraph(
            "Loan Portfolio Health Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    # =================================
    # EXECUTIVE SUMMARY
    # =================================

    elements.append(
        Paragraph(
            "Executive Summary",
            styles["Heading1"]
        )
    )

    summary_data = [
        ["Metric", "Value"],
        ["Total Loans", f"{total_loans:,}"],
        ["Total Loan Value", f"${total_loan_value:,.0f}"],
        ["NPA Rate", f"{overall_npa_rate}%"],
        ["Average Recovery", f"${avg_recovery:,.0f}"],
        ["Health Score", f"{health_score}/100"]
    ]

    summary_table = Table(summary_data)

    summary_table.setStyle(
        TableStyle([
            ("GRID", (0,0), (-1,-1), 1, colors.black),
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")
        ])
    )

    elements.append(summary_table)

    elements.append(Spacer(1, 20))

    # =================================
    # PORTFOLIO STATUS
    # =================================

    elements.append(
        Paragraph(
            "Portfolio Status",
            styles["Heading1"]
        )
    )

    if health_score >= 80:
        status = "Healthy"

    elif health_score >= 60:
        status = "Moderate Risk"

    else:
        status = "High Risk"

    elements.append(
        Paragraph(
            f"Current Status: {status}",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 20))

    # =================================
    # RISK DISTRIBUTION
    # =================================

    elements.append(
        Paragraph(
            "Risk Distribution",
            styles["Heading1"]
        )
    )

    risk_data = [
        ["Risk Category", "Count"],
        ["Low Risk", f"{low_risk_count:,}"],
        ["Medium Risk", f"{medium_risk_count:,}"],
        ["High Risk", f"{high_risk_count:,}"]
    ]

    risk_table = Table(risk_data)

    risk_table.setStyle(
        TableStyle([
            ("GRID", (0,0), (-1,-1), 1, colors.black),
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")
        ])
    )

    elements.append(risk_table)

    elements.append(Spacer(1, 20))

    # =================================
    # ALERTS
    # =================================

    elements.append(
        Paragraph(
            "Alerts",
            styles["Heading1"]
        )
    )

    alerts = []

    if overall_npa_rate > 10:
        alerts.append("• NPA Rate Above Threshold")

    if high_risk_count > 10000:
        alerts.append("• Large Number of High Risk Accounts")

    if health_score < 60:
        alerts.append("• Portfolio Health Requires Attention")

    if len(alerts) == 0:
        alerts.append("• No Critical Alerts")

    for alert in alerts:
        elements.append(
            Paragraph(
                alert,
                styles["BodyText"]
            )
        )

    elements.append(Spacer(1, 20))

    # =================================
    # RECOMMENDATIONS
    # =================================

    elements.append(
        Paragraph(
            "Recommendations",
            styles["Heading1"]
        )
    )

    recommendations = [
        "Monitor Grade F and Grade G loans closely.",
        "Reduce exposure to high-risk borrowers.",
        "Improve recovery performance.",
        "Strengthen collection strategy.",
        "Review debt consolidation loan segment."
    ]

    for rec in recommendations:
        elements.append(
            Paragraph(
                f"• {rec}",
                styles["BodyText"]
            )
        )

    doc.build(elements)

    buffer.seek(0)

    return buffer