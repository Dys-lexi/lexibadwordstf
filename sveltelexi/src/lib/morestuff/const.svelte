<script module lang="ts">
  import ionLogo from "$lib/images/ion_cropped_croppedsmall.png";
  import legionLogo from "$lib/images/legion_cropped_croppedsmall.png";
  import northstarLogo from "$lib/images/northstar2_cropped_croppedsmall.png";
  import roninLogo from "$lib/images/ronin2_cropped_croppedsmall.png";
  import scorchLogo from "$lib/images/scorch2_cropped_croppedsmall.png";
  import toneLogo from "$lib/images/tone2_cropped_croppedsmall.png";
  import demomanLogo from "$lib/images/demoman.png";
  import engineerLogo from "$lib/images/engineer.png";
  import heavyweaponsLogo from "$lib/images/heavyweapons.png";
  import medicLogo from "$lib/images/medic.png";
  import pyroLogo from "$lib/images/pyro.png";
  import scoutLogo from "$lib/images/scout.png";
  import sniperLogo from "$lib/images/sniper.png";
  import soldierLogo from "$lib/images/soldier.png";
  import spyLogo from "$lib/images/spy.png";
  // import copylogo from "$lib/images/copy.svg";

  export { ClassLogo, Logo,copy };

  const logos = [ionLogo, toneLogo, legionLogo, scorchLogo, roninLogo, northstarLogo] as const;
  const fallbackLogo = logos[0];
  const classLogos = {
    demoman: demomanLogo,
    engineer: engineerLogo,
    heavyweapons: heavyweaponsLogo,
    medic: medicLogo,
    pyro: pyroLogo,
    scout: scoutLogo,
    sniper: sniperLogo,
    soldier: soldierLogo,
    spy: spyLogo
  } as const;


</script>

{#snippet Logo(randomnumber =  Math.floor(Math.random() * 1000))}
<div>
      <a href="/">
        <img  src={logos[randomnumber%logos.length]} height={64} width={64} alt="" />
      </a>
    </div>
{/snippet}

{#snippet ClassLogo(name: string)}
  {@const logo = classLogos[name.replace(/\.png$/, "").toLowerCase() as keyof typeof classLogos]}
  {#if logo}
    <img  style="height: 100%; width: 100%; object-fit:contain" src={logo} height={64} width={64} alt={name.replace(/\.png$/, "")} />
  {/if}
{/snippet}


{#snippet copy()}

     
       <svg stroke="rgba(170,170,170,1)" style="max-height:100%" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"  stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-copy-icon lucide-copy"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
    
  
{/snippet}
