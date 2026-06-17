import { useData } from "vike-react/useData";
import type { Data } from "./+data.js";

export default function Page() {
  const  {personresults ,statuscode} = useData<Data>();
  
  return (
    <> 
      <img src={personresults.avatarurl}></img>
          <p>{statuscode}</p>
          <div>{JSON.stringify(personresults)}</div>
    </>
  );
}
