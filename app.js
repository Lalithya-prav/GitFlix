async function loadGitFlixData() {
  try {
    const response = await fetch('gitflix_data.json');
    if (!response.ok) throw new Error("Could not find gitflix_data.json");

    const data = await response.json();
    const stats = data.stats;
    const commits = data.commits;

    // 1. Populate Metrics
    document.getElementById('total-commits').textContent = stats.total_commits;
    document.getElementById('contributors').textContent = stats.unique_contributors;
    document.getElementById('lifespan').textContent = `${stats.lifespan_days} day(s)`;
    document.getElementById('net-lines').textContent = `+${stats.net_lines}`;

    // 2. Render Recent Commits List
    const commitsListEl = document.getElementById('commits-list');
    commitsListEl.innerHTML = ''; // clear

    // Show latest 5 commits
    const recentCommits = [...commits].reverse().slice(0, 5);
    recentCommits.forEach(c => {
      const item = document.createElement('div');
      item.className = 'commit-item';
      item.innerHTML = `
        <div>
          <strong>${c.message}</strong>
          <div class="commit-meta">by ${c.author} on ${c.date}</div>
        </div>
        <span style="color:#58a6ff; font-family:monospace;">${c.sha}</span>
      `;
      commitsListEl.appendChild(item);
    });

    // 3. Render Chart
    renderGrowthChart(commits);

  } catch (err) {
    console.error("Error loading GitFlix data:", err);
  }
}

function renderGrowthChart(commits) {
  let cumulativeLines = 0;
  const labels = [];
  const lineCounts = [];

  commits.forEach((c, i) => {
    cumulativeLines += (c.insertions - c.deletions);
    labels.push(`Commit #${i + 1}`);
    lineCounts.push(cumulativeLines);
  });

  const ctx = document.getElementById('growthChart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Net Codebase Lines',
        data: lineCounts,
        borderColor: '#3fb950',
        backgroundColor: 'rgba(63, 185, 80, 0.1)',
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { ticks: { color: '#8b949e' } },
        y: { ticks: { color: '#8b949e' } }
      },
      plugins: {
        legend: { labels: { color: '#c9d1d9' } }
      }
    }
  });
}

// Load data when page opens
document.addEventListener('DOMContentLoaded', loadGitFlixData);