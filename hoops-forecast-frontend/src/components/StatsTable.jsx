const FIELDS = [
  ["season", "Season"],
  ["age", "Age"],
  ["pos", "Pos"],
  ["g", "GP"],
  ["mp_per_game", "MIN"],
  ["pts_per_game", "PTS"],
  ["ast_per_game", "AST"],
  ["trb_per_game", "REB"],
  ["stl_per_game", "STL"],
  ["blk_per_game", "BLK"],
  ["fg_percent", "FG%"],
  ["x3p_percent", "3P%"],
  ["ft_percent", "FT%"]
];

export default function StatsTable({ rows }) {
  if (!rows || rows.length === 0) return null;

  return (
    <div className="stats-table__wrap">
      <table className="stats-table">
        <thead>
          <tr>
            {FIELDS.map(([key, label]) => (
              <th key={key}>{label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i}>
              {FIELDS.map(([key]) => (
                <td key={key}>{row[key] ?? "-"}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
