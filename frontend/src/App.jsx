import { useState } from "react";
import axios from "axios";
import "./App.css";
import logo from "./assets/logo.png";

const USD_TO_ZAR = 16.51;
const SA_MARKET_ADJUSTMENT = 0.25;

function App() {
  const [file, setFile] = useState(null);
  const [cvData, setCvData] = useState(null);
  const [salaryResponse, setSalaryResponse] = useState(null);
  const [currency, setCurrency] = useState("USD");
  const [isUploading, setIsUploading] = useState(false);
const [isPredicting, setIsPredicting] = useState(false);

  const [contextData, setContextData] = useState({
    job_title: "Software Engineer",
    industry: "Technology",
    company_size: "Medium",
    location: "South Africa",
    remote_work: "No",
  });

  const handleContextChange = (e) => {
      setContextData({
        ...contextData,
        [e.target.name]: e.target.value,
      });
    };

    const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select a CV first");
      return;
    }

    const formDataToSend = new FormData();
    formDataToSend.append("file", file);

    try {
      setIsUploading(true);

      const res = await axios.post(
        "http://127.0.0.1:8000/upload-cv",
        formDataToSend,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setCvData(res.data);
      setSalaryResponse(null);
    } catch (error) {
      console.error(error);
      alert("Upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  const handlePredictSalary = async () => {
  try {
    setIsPredicting(true);

    const payload = {
      skills: cvData.skills,
      experience_years: cvData.experience_years,
      education_level: cvData.education_level,
      certifications: cvData.certifications,
      ...contextData,
    };

    const res = await axios.post(
      "http://127.0.0.1:8000/predict-salary",
      payload
    );

    setSalaryResponse(res.data);
  } catch (error) {
    console.error(error);
    alert("Salary prediction failed");
  } finally {
    setIsPredicting(false);
  }
};

  const getSalaryValues = () => {
    if (!salaryResponse?.predicted_salary) return null;

    const yearlyUSD = salaryResponse.predicted_salary;
    const monthlyUSD = yearlyUSD / 12;

    const yearlyZAR = yearlyUSD * USD_TO_ZAR * SA_MARKET_ADJUSTMENT;
    const monthlyZAR = yearlyZAR / 12;

    if (currency === "USD") {
      return {
        symbol: "$",
        yearly: yearlyUSD,
        monthly: monthlyUSD,
      };
    }

    return {
      symbol: "R",
      yearly: yearlyZAR,
      monthly: monthlyZAR,
    };
  };

  const salary = getSalaryValues();

  return (
    <div className="app">
      <div className="hero">
        <div className="hero-content">
            <div className="logo-section">
              <img src={logo} alt="CV Salary Predictor Logo" className="logo" />
            </div>

            {/* <span className="badge">AI Powered CV Analysis</span> */}

            <h1>CV Salary Predictor</h1>
          <p>
            Upload your CV to estimate salary benchmarks for IT and software
            roles. This tool is not designed for unrelated fields such as law,
            medicine, finance, or general non-technical careers.
          </p>
        </div>

        <div className="card">
          <form onSubmit={handleUpload}>
            <label className="upload-box">
              <input
                type="file"
                accept=".pdf,.docx"
                onChange={(e) => setFile(e.target.files[0])}
              />
              <span>{file ? file.name : "Choose your CV file"}</span>
              <small>PDF or DOCX only</small>
            </label>

            <button type="submit" disabled={isUploading}>
              {isUploading ? "Analyzing CV..." : "Analyze CV"}
            </button>
            <button
              type="button"
              className="secondary-btn"
              onClick={() => {
                setFile(null);
                setCvData(null);
                setSalaryResponse(null);
              }}
            >
              Reset
            </button>
          </form>

          {cvData && (
            <div className="result">
              <h3>CV Analysis Complete</h3>

              <div className="info">
                <p>
                  <strong>File:</strong> {cvData.filename}
                </p>
                <p>
                  <strong>Experience:</strong> {cvData.experience_years} years
                </p>
                <p>
                  <strong>Education:</strong> {cvData.education_level}
                </p>
                <p>
                  <strong>Certifications:</strong> {cvData.certifications}
                </p>
              </div>

              <h4>Detected Skills</h4>
              <div className="skills">
                {cvData.skills.length > 0 ? (
                  cvData.skills.map((skill, index) => (
                    <span key={index}>{skill}</span>
                  ))
                ) : (
                  <p>No skills detected yet.</p>
                )}
              </div>

              <h4>Confirm Prediction Context</h4>

              <div className="context-form">

                <div className="field">
                  <label>Target Job Title</label>

                  <select
                    name="job_title"
                    value={contextData.job_title}
                    onChange={handleContextChange}
                  >
                    <option>Software Engineer</option>
                    <option>Frontend Developer</option>
                    <option>Backend Developer</option>
                    <option>Full Stack Developer</option>
                    <option>Web Developer</option>
                    <option>Mobile App Developer</option>
                    <option>Data Analyst</option>
                    <option>Data Scientist</option>
                    <option>Machine Learning Engineer</option>
                    <option>AI Engineer</option>
                    <option>DevOps Engineer</option>
                    <option>Cloud Engineer</option>
                    <option>Cybersecurity Analyst</option>
                    <option>UI/UX Designer</option>
                    <option>QA Engineer</option>
                    <option>Business Analyst</option>
                    <option>Systems Analyst</option>
                    <option>Database Administrator</option>
                    <option>IT Support Specialist</option>
                    <option>Network Engineer</option>
                  </select>
                </div>

                <div className="field">
                  <label>Industry</label>
                  <select
                    name="industry"
                    value={contextData.industry}
                    onChange={handleContextChange}
                  >
                    <option>Technology</option>
                    <option>Finance</option>
                    <option>Healthcare</option>
                    <option>Education</option>
                    <option>Retail</option>
                    <option>Consulting</option>
                    <option>Manufacturing</option>
                  </select>
                </div>

                <div className="field">
                  <label>Company Size</label>
                  <select
                    name="company_size"
                    value={contextData.company_size}
                    onChange={handleContextChange}
                  >
                    <option>Small</option>
                    <option>Medium</option>
                    <option>Large</option>
                  </select>
                </div>

                <div className="field">
                  <label>Work Location</label>
                  <select
                    name="location"
                    value={contextData.location}
                    onChange={handleContextChange}
                  >
                    <option>South Africa</option>
                    <option>United States</option>
                    <option>United Kingdom</option>
                    <option>Canada</option>
                    <option>Germany</option>
                    <option>Australia</option>
                    <option>India</option>
                  </select>
                </div>

                <div className="field">
                  <label>Remote Work</label>
                  <select
                    name="remote_work"
                    value={contextData.remote_work}
                    onChange={handleContextChange}
                  >
                    <option>No</option>
                    <option>Yes</option>
                  </select>
                </div>

              </div>

              <button
                type="button"
                onClick={handlePredictSalary}
                disabled={!cvData.document_validation?.is_valid || isPredicting}
              >
                {isPredicting ? "Predicting Salary..." : "Predict Salary"}
              </button>
            </div>
          )}

          {isUploading && (
            <div className="loading-box">
              <div className="spinner"></div>
              <p>Analyzing your CV, extracting skills and checking quality...</p>
            </div>
          )}

          {cvData?.document_validation && !cvData.document_validation.is_valid && (
            <div className="warning-box">
              <h4>Unsupported Document</h4>
              <p>
                This file does not appear to be an IT/software-related CV. Salary prediction
                is disabled because the results would not be reliable.
              </p>
            </div>
          )}

            {isPredicting && (
              <div className="loading-box">
                <div className="spinner"></div>
                <p>Generating salary prediction...</p>
              </div>
            )}

          {cvData && cvData.cv_quality && (
            <div className={cvData.cv_quality.is_poor_cv ? "warning-box" : "quality-box"}>
              <h4>CV Quality Check</h4>
              <p>
                Reliability Score: <strong>{cvData.cv_quality.reliability_score}%</strong>
              </p>

              {cvData.cv_quality.issues.length > 0 ? (
                <ul>
                  {cvData.cv_quality.issues.map((issue, index) => (
                    <li key={index}>{issue}</li>
                  ))}
                </ul>
              ) : (
                <p>Your CV has enough information for a basic prediction.</p>
              )}
            </div>
          )}

          {cvData && cvData.portfolio_suggestions &&(
            <div className="suggestion-box">
              <h4>Suggestions to Build a Stronger Portfolio</h4>
              <ul>
                {cvData.portfolio_suggestions.map((suggestion, index) => (
                  <li key={index}>{suggestion}</li>
                ))}
              </ul>
            </div>
          )}

          {salaryResponse && salary && (
            <div className="result">
              <h3>Salary Prediction</h3>

              <div className="currency-toggle">
                <button
                  className={currency === "USD" ? "active" : ""}
                  onClick={() => setCurrency("USD")}
                >
                  USD
                </button>
                <button
                  className={currency === "ZAR" ? "active" : ""}
                  onClick={() => setCurrency("ZAR")}
                >
                  ZAR
                </button>
              </div>

              <div className="salary-grid">
                <div>
                  <p>Monthly Salary</p>
                  <h2>
                    {salary.symbol}
                    {salary.monthly.toLocaleString(undefined, {
                      maximumFractionDigits: 2,
                    })}
                  </h2>
                </div>

                <div>
                  <p>Yearly Salary</p>
                  <h2>
                    {salary.symbol}
                    {salary.yearly.toLocaleString(undefined, {
                      maximumFractionDigits: 2,
                    })}
                  </h2>
                </div>
                <p className="salary-disclaimer">
                  Salary predictions are AI-generated estimates for IT/software-related roles
                  and should not be considered guaranteed compensation figures.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
      <footer className="footer">
        Created by <strong>Thabani Ndlozi</strong>
      </footer>
    </div>
  );
}

export default App;