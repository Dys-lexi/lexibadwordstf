<script module lang="ts">
  import ionLogo from "$lib/images/ion_cropped_croppedsmall.png";
  import legionLogo from "$lib/images/legion_cropped_croppedsmall.png";
  import northstarLogo from "$lib/images/northstar2_cropped_croppedsmall.png";
  import roninLogo from "$lib/images/ronin2_cropped_croppedsmall.png";
  import scorchLogo from "$lib/images/scorch2_cropped_croppedsmall.png";
  import toneLogo from "$lib/images/tone2_cropped_croppedsmall.png";

  export { Logo };

  const logos = [ionLogo, toneLogo, legionLogo, scorchLogo, roninLogo, northstarLogo] as const;
  const fallbackLogo = logos[0];


</script>

{#snippet Logo(randomnumber =  Math.floor(Math.random() * 1000))}
<div>
      <a href="/">
        <img  src={logos[randomnumber%logos.length]} height={64} width={64} alt="" />
      </a>
    </div>
{/snippet}
