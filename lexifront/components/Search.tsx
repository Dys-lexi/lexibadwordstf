import { navigate } from 'vike/client/router'
import React from "react";

interface testProps {
    classNameform?: string;
    classNameinput?: string;
    classnamebutton?: string;
}

// export const Test: React.FC<testProps> = ({ className }) => {
//   return <div className={className}>Test</div>;
// };

export default function Prettysearch({ classNameform, classNameinput, classnamebutton } : testProps) {

   async function onSubmit(formData:FormData) {
  const navigationPromise = navigate(`/${encodeURIComponent(formData.get("user") as string)}`)
  console.log("The URL changed but the new page hasn't rendered yet.")
  await navigationPromise
  console.log('The new page has finished rendering.')
}

  return (
    <>
     <form action={onSubmit} className={classNameform}>
    <input name="user" className={classNameinput}/>
    <button type="submit" className={classnamebutton}>Search</button>
      </form>
      </>
  )
}