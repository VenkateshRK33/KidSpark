/**
 * Chart.js initialization for KidSpark Performance Dashboard
 * Handles subject performance bar chart and improvement line chart
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts if data is available
    if (window.subjectData && window.subjectData.length > 0) {
        initSubjectBarChart();
    }
    
    if (window.improvementData && Object.keys(window.improvementData).length > 0) {
        initImprovementLineChart();
    }
});

/**
 * Initialize horizontal bar chart for subject performance
 */
function initSubjectBarChart() {
    const ctx = document.getElementById('subjectBarChart');
    if (!ctx) return;
    
    // Prepare data
    const subjects = window.subjectData.map(item => item.subject);
    const averages = window.subjectData.map(item => parseFloat(item.avg_pct));
    
    // Color code based on performance
    const backgroundColors = averages.map(avg => {
        if (avg >= 70) return 'rgba(76, 175, 80, 0.8)';  // Green
        if (avg >= 50) return 'rgba(255, 152, 0, 0.8)';  // Orange
        return 'rgba(244, 67, 54, 0.8)';  // Red
    });
    
    const borderColors = averages.map(avg => {
        if (avg >= 70) return 'rgba(76, 175, 80, 1)';
        if (avg >= 50) return 'rgba(255, 152, 0, 1)';
        return 'rgba(244, 67, 54, 1)';
    });
    
    // Create chart
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: subjects,
            datasets: [{
                label: 'Average Score (%)',
                data: averages,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 2
            }]
        },
        options: {
            indexAxis: 'y',  // Horizontal bars
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Subject Performance Overview',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const item = window.subjectData[context.dataIndex];
                            return [
                                `Average: ${context.parsed.x}%`,
                                `Best: ${item.best_pct.toFixed(1)}%`,
                                `Attempts: ${item.attempts}`
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * Initialize line chart for improvement over time
 */
function initImprovementLineChart() {
    const ctx = document.getElementById('improvementLineChart');
    if (!ctx) return;
    
    // Prepare datasets for each subject
    const datasets = [];
    const colors = [
        { bg: 'rgba(102, 126, 234, 0.2)', border: 'rgba(102, 126, 234, 1)' },  // Purple
        { bg: 'rgba(76, 175, 80, 0.2)', border: 'rgba(76, 175, 80, 1)' },      // Green
        { bg: 'rgba(255, 152, 0, 0.2)', border: 'rgba(255, 152, 0, 1)' },      // Orange
        { bg: 'rgba(33, 150, 243, 0.2)', border: 'rgba(33, 150, 243, 1)' },    // Blue
        { bg: 'rgba(233, 30, 99, 0.2)', border: 'rgba(233, 30, 99, 1)' },      // Pink
        { bg: 'rgba(156, 39, 176, 0.2)', border: 'rgba(156, 39, 176, 1)' }     // Deep Purple
    ];
    
    let colorIndex = 0;
    
    for (const [subject, data] of Object.entries(window.improvementData)) {
        const color = colors[colorIndex % colors.length];
        
        datasets.push({
            label: subject,
            data: data.data,
            borderColor: color.border,
            backgroundColor: color.bg,
            borderWidth: 3,
            fill: true,
            tension: 0.4,  // Smooth curves
            pointRadius: 5,
            pointHoverRadius: 7,
            pointBackgroundColor: color.border,
            pointBorderColor: '#fff',
            pointBorderWidth: 2
        });
        
        colorIndex++;
    }
    
    // Get all unique dates across all subjects
    const allLabels = new Set();
    for (const data of Object.values(window.improvementData)) {
        data.labels.forEach(label => allLabels.add(label));
    }
    const sortedLabels = Array.from(allLabels).sort();
    
    // Create chart
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: sortedLabels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Score Improvement Over Time',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.parsed.y}%`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date',
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Score (%)',
                        font: {
                            weight: 'bold'
                        }
                    },
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            }
        }
    });
}
