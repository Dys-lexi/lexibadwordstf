import "./Page.css";
import { useData } from "vike-react/useData";
import { navigate } from "vike/client/router";
import Search from "../../components/Search";
import type { Data } from "./+data.js";
export default function Page() {
  const { stats, statuscode } = useData<Data>();
  return (
    <div className="flexbox" style={{ gap: "30px" }}>
      <Search
        classNameform="bigsearchform"
        classNameinput="bigsearchinput"
        classnamebutton="bigsearchbutton"
      />
      <div className="statsholder">
        {statuscode == 200 ? (
          Object.entries(stats).map(([stat, val], index) => (
            <div key={index} className="stat">
              <div className="statsname"> {getstatprettyname(stat)}: </div>{" "}
              <div className="statsstat"> {val.toLocaleString()} </div>
            </div>
          ))
        ) : (
          <div className="stat" style={{ color: "red" }}>
            Backend is probably down :( {statuscode}
          </div>
        )}
      </div>
      <div className="nonowordtimestamp loglink">
        Made by{" "}
        <u style={{ textDecorationColor: "rgba(255,180,200,0.8)" }}>
          <a
            href="https://discord.gg/uR7KwhedfK"
            target="_blank"
            style={{ color: "rgba(255,180,200,1)" }}
          >
            @dyslexi
          </a>
        </u>{" "}
        on discord
      </div>
    </div>
  );
}

function getstatprettyname(name: string): string {
  const names: Record<string, string> = {
    uniquepeople: "Unique Players",
    totalmessages: "Total Messages",
    totalmatches: "Logs Searched",
    badmessages: "Flagged messages",
    flaggedplayers: "Flagged Players",
  };

  return names[name] || name;
}
