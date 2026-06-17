import "./Layout.css";

import { Link } from "../components/Link";
import { ClientOnly } from "vike-react/ClientOnly";
// import Search from "../components/Search";
import { Prettybackground,Content,Logo } from "../components/const";
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

        <Content>{children}</Content>
      </div>
    </>
  );
}



