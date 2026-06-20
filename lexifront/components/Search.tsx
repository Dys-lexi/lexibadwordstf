import { navigate } from "vike/client/router";
import React from "react";
import { usewsstore } from "./websocketsearch";
interface testProps {
  classNameform?: string;
  classNameinput?: string;
  classnamebutton?: string;
}

// export const Test: React.FC<testProps> = ({ className }) => {
//   return <div className={className}>Test</div>;
// };

export default function Prettysearch({
  classNameform,
  classNameinput,
  classnamebutton,
}: testProps) {
  const [isFocused, setIsFocused] = React.useState(false);

  async function onSubmit(formData: FormData) {
    disconnect();
    const username = formData.get("user") as string;
    const match = matches.find(({ n }) => n.toLocaleLowerCase() === username.toLocaleLowerCase());
    const id = match ? match.id : username;
    const navigationPromise = navigate(
      `/${encodeURIComponent(id)}`,
    );
    console.log("The URL changed but the new page hasn't rendered yet.");
    await navigationPromise;
    console.log("The new page has finished rendering.");
  }
  async function onsuggest(formData: string) {
    disconnect();
    const navigationPromise = navigate(`/${encodeURIComponent(formData)}`);
    console.log("The URL changed but the new page hasn't rendered yet.");
    await navigationPromise;
    console.log("The new page has finished rendering.");
  }
  const { connect, disconnect, matches, sendsearch , count} =
    usewsstore();


  function focused() {
    connect();
    setIsFocused(true);
  }

  function blurred() {
    setTimeout(() => setIsFocused(false), 200);
  }
  return (
    <div className="flexstuff" onBlur={blurred}>
      <form action={onSubmit} className={classNameform}>
        <input
          autoCorrect="off"
          spellCheck="false"
          autoComplete="off"
          name="user"
          onFocus={(e) => {
            focused();
            sendsearch(e.target.value);
          }}
          onChange={(e) => {
            focused();
            sendsearch(e.target.value);
          }}
          className={classNameinput}
          placeholder="Enter somones profile link, or a steamid"
        />
        <button type="submit" className={classnamebutton}>
          Search
        </button>
      </form>
      <div style={{ position: "relative", width: "100%" }}>
        {isFocused  && matches.length ?  (
          <div className="searchsuggestionholder">
            {" "}
          
            {matches.map(({ n, id, a, g }, index) => {
              return (
                <a
                  className={`suggestion${!index ? " importantsuggestion" : ""}`}
                  onClick={() => {
                    onsuggest(id);
                  }}
                  key={index}
                >
                  <img style={{ "height": "100%" }}
                    src={`https://avatars.fastly.steamstatic.com/${a ? a : "fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb"}.jpg`}
                  ></img>
                  <div
                    
                  
                  >
                    {n}
                  </div>
                  <span className="logcounter">{g == 1 ? "1 Log" : `${g} Logs`}</span>
                  {/* {" "} <span className="">{id}</span> */}
                  {" "}
                </a>
              );
            })}{" "}  <div className="notice">Log counts are grouped by username</div>
          </div>
) : (
          ""
        )}
      </div>
    </div>
  );
}
