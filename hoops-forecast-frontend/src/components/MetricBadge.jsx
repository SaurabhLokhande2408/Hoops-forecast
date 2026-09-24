export default function MetricBadge({ label, value }) {
  return (
    <div className="metric-badge">
      <span className="metric-badge__value">{value}</span>
      <span className="metric-badge__label">{label}</span>
    </div>
  );
}
