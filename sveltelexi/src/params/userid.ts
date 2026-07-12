import type { ParamMatcher } from '@sveltejs/kit';

const nonos = [
"ion_cropped_croppedsmall.png",
"ion_cropped.png",
"legion_cropped_croppedsmall.png",
"legion_cropped.png",
"northstar2_cropped_croppedsmall.png",
"northstar2_cropped.png",
"ronin2_cropped_croppedsmall.png",
"ronin2_cropped.png",
"scorch2_cropped_croppedsmall.png",
"scorch2_cropped.png",
"tone2_cropped_croppedsmall.png",
"tone2_cropped.png",
"favicon.ico",
"sitemap.xml",
"0",
"00000000000000000"


] as Array<string>


export const match = ((param: string): param is string => {
	return !nonos.includes(param)
}) satisfies ParamMatcher;