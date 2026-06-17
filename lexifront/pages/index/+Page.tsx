import "./Page.css";
import { navigate } from 'vike/client/router'
import Search from "../../components/Search";

export default function Page() {
  return (
    <div className="flexbox">
       <Search  classNameform = "bigsearchform" classNameinput = "bigsearchinput"  classnamebutton = "bigsearchbutton"  />
      
    </div>
  );
}

