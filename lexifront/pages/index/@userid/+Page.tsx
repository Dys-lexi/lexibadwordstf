import { useData } from "vike-react/useData";
import { usePageContext } from "vike-react/usePageContext";
import type { Data } from "./+data.js";
import "./Page.css";
export default function Page() {
  const { personresults, statuscode } = useData<Data>();
  const pageContext = usePageContext();
  if (statuscode == 200) {
    return (
      <div className="nonoresultsholder">
        <div className="nameholderbad">
          <div className="nonowordavatarholder">
            <img src={personresults.frame} className="avatarholder" ></img>
          <img src={personresults.avatarurl} className="nonowordavatar" ></img>
          </div>
          <div className="nonowordcurrentusername" > { personresults.currentusername}</div>
        </div>
        {/* <p>{statuscode}</p> */}
        {/* <div>{JSON.stringify(personresults)}</div> */}
        {/* https://steamcommunity.com/id/thebv */}
        <div className="nonowordsholder">
          {personresults.nonowords != null && personresults.nonowords.length ?
            personresults.nonowords.map((badword, index) => (
              <div key={index} className="nonowordbox">
                <a className="nonowordtimestamp loglink" target="_blank" href={`https://logs.tf/${badword.matchid}`}>log</a>
                <div className="nonowordtimestamp">{new Date(badword.timestamp * 1000).toLocaleDateString()}</div>
                <div className="nonowordmessage"> <div className="nonowordname">{badword.name}</div>: {badword.message}</div>
              </div>
            )) : <h2>No bad words found for { personresults.currentusername}</h2>}
        </div>
      </div>
    );
  }
  else {
    return (<h2>could not find user "{ pageContext.routeParams.userid}"</h2>)
  }
}
