let chartInstance = null;
let animationTimer = null;

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
    commitsListEl.innerHTML = '';

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

    // 3. Render Initial Full Chart
    renderGrowthChart(commits);

    // 4. Attach Replay Listener
    const playBtn = document.getElementById('play-btn');
    playBtn.addEventListener('click', () => startReplay(commits));

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
  
  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
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

function startReplay(commits) {
  const playBtn = document.getElementById('play-btn');
  playBtn.disabled = true;
  playBtn.textContent = '⏳ Playing...';

  if (animationTimer) clearInterval(animationTimer);

  let step = 0;
  let cumulativeLines = 0;
  const labels = [];
  const lineCounts = [];

  // Reset Chart to empty state
  chartInstance.data.labels = [];
  chartInstance.data.datasets[0].data = [];
  chartInstance.update();

  // Animate frame-by-frame every 600ms
  animationTimer = setInterval(() => {
    if (step >= commits.length) {
      clearInterval(animationTimer);
      playBtn.disabled = false;
      playBtn.textContent = '🔄 Replay Again';
      return;
    }

    const c = commits[step];
    cumulativeLines += (c.insertions - c.deletions);
    labels.push(`Commit #${step + 1}`);
    lineCounts.push(cumulativeLines);

    chartInstance.data.labels = [...labels];
    chartInstance.data.datasets[0].data = [...lineCounts];
    chartInstance.update();

    step++;
  }, 1200);
}

document.addEventListener('DOMContentLoaded', loadGitFlixData);