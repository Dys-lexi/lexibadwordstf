import "../../Layout.css";
import "../Page.css";
import Search from "../../../components/Search"
import logoUrl from "../../../assets/logo.png";

import { ClientOnly } from "vike-react/ClientOnly";
import { Prettybackground,Content,Logo } from "../../../components/const";
// import Search from "../components/Search";
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <ClientOnly>
        <Prettybackground />
      </ClientOnly>
      <div
        className="mainthing"
      >
        <div style={{ display: "flex", justifyContent: "center", "gap":"10px" }}>
          <Logo />
          <h1>lexislurs for team fortress 2</h1>
        </div>
        <div className="flexbox">
  <Search  classNameform = "littlesearchform" classNameinput = "littlesearchinput"  classnamebutton = "littlesearchbutton"  /></div>
        <Content>{children}</Content>
      </div>
    </>
  );
}

