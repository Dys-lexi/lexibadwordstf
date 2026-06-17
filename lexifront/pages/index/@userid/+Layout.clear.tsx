import "../../Layout.css";
import Search from "../../../components/Search"
import logoUrl from "../../../assets/logo.svg";

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
        <div style={{ display: "flex", justifyContent: "center" }}>
          <Logo />
          <h1>lexislurs</h1>
          
        </div>
  <Search  classNameform = "bigsearchform" classNameinput = "bigsearchinput"  classnamebutton = "bigsearchbutton"  />
        <Content>{children}</Content>
      </div>
    </>
  );
}

