const API_URL = "http://127.0.0.1:8000";

const solutionInput = document.getElementById("solution");
const charCount = document.getElementById("charCount");
const analyzeBtn = document.getElementById("analyzeBtn");

const loadingSection = document.getElementById("loadingSection");
const reportSection = document.getElementById("reportSection");

const newAnalysisBtn = document.getElementById("newAnalysisBtn");


/* =========================
   CHARACTER COUNTER
========================= */

solutionInput.addEventListener("input", () => {

    const count = solutionInput.value.length;

    charCount.textContent = `${count} characters`;

});


/* =========================
   ANALYZE BUTTON
========================= */

analyzeBtn.addEventListener("click", analyzeSolution);


async function analyzeSolution() {

    const solution = solutionInput.value.trim();

    if (!solution) {

        alert("Please describe your AI solution first.");

        return;
    }


    analyzeBtn.disabled = true;

    loadingSection.classList.remove("hidden");

    reportSection.classList.add("hidden");


    try {

        const response = await fetch(`${API_URL}/api/analyze`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                solution: solution
            })

        });


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                data.error ||
                "Analysis failed"
            );

        }


        displayReport(data);


    } catch (error) {

        console.error(error);

        alert(
            "Something went wrong:\n\n" +
            error.message
        );

    } finally {

        analyzeBtn.disabled = false;

        loadingSection.classList.add("hidden");

    }

}


/* =========================
   DISPLAY REPORT
========================= */

function displayReport(data) {

    reportSection.classList.remove("hidden");


    /*
       Your backend may return the report
       directly OR inside data.report.
    */

    const report = data.report || data;


    /* SCORE */

    const score =
        report.overall_score ??
        report.stress_score ??
        report.score ??
        0;

    document.getElementById("overallScore")
        .textContent = score;


    /* RISK LEVEL */

    const level =
        report.risk_level ||
        getRiskLevel(score);

    document.getElementById("riskLevel")
        .textContent = level;


    document.getElementById("riskMessage")
        .textContent = getRiskMessage(level);


    /* BREAKDOWN */

    const breakdown =
        report.risk_breakdown ||
        report.risks ||
        {};


    setScore(
        "technicalScore",
        breakdown.technical
    );

    setScore(
        "costScore",
        breakdown.cost
    );

    setScore(
        "privacyScore",
        breakdown.privacy
    );

    setScore(
        "securityScore",
        breakdown.security
    );

    setScore(
        "fairnessScore",
        breakdown.fairness
    );

    setScore(
        "operationalScore",
        breakdown.operational
    );


    /* LISTS */

    fillList(
        "criticalRisks",
        report.critical_risks ||
        report.criticalRisks ||
        []
    );


    fillList(
        "topRisks",
        report.top_risks ||
        report.topRisks ||
        []
    );


    fillList(
        "strengths",
        report.strengths ||
        []
    );


    fillList(
        "actions",
        report.recommended_actions ||
        report.recommendations ||
        report.actions ||
        []
    );


    /* VERDICT */

    document.getElementById("finalVerdict")
        .textContent =
        report.final_verdict ||
        report.finalVerdict ||
        "Analysis completed successfully.";


    /* SCROLL */

    reportSection.scrollIntoView({
        behavior: "smooth"
    });

}


/* =========================
   SCORE HELPER
========================= */

function setScore(id, value) {

    const element = document.getElementById(id);

    if (value === undefined || value === null) {

        element.textContent = "--/100";

        return;
    }


    if (typeof value === "object") {

        value =
            value.score ??
            value.value ??
            0;

    }


    element.textContent = `${value}/100`;

}


/* =========================
   LIST HELPER
========================= */

function fillList(id, items) {

    const element = document.getElementById(id);

    element.innerHTML = "";


    if (!items || items.length === 0) {

        const li = document.createElement("li");

        li.textContent = "No items identified.";

        element.appendChild(li);

        return;
    }


    items.forEach(item => {

        const li = document.createElement("li");

        if (typeof item === "object") {

            li.textContent =
                item.description ||
                item.text ||
                item.risk ||
                JSON.stringify(item);

        } else {

            li.textContent = item;

        }

        element.appendChild(li);

    });

}


/* =========================
   RISK LEVEL
========================= */

function getRiskLevel(score) {

    if (score >= 75) {
        return "Critical";
    }

    if (score >= 50) {
        return "High";
    }

    if (score >= 25) {
        return "Medium";
    }

    return "Low";
}


function getRiskMessage(level) {

    switch (level.toLowerCase()) {

        case "critical":
            return "Major Risks Detected";

        case "high":
            return "Proceed with Caution";

        case "medium":
            return "Review Before Deployment";

        case "low":
            return "Low Risk Detected";

        default:
            return "Review Assessment";

    }

}


/* =========================
   NEW ANALYSIS
========================= */

newAnalysisBtn.addEventListener("click", () => {

    solutionInput.value = "";

    charCount.textContent = "0 characters";

    reportSection.classList.add("hidden");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

});