import { query } from '$app/server';
import { API_URL } from '$lib/morestuff/config';
import type { Userdetails } from '$lib/morestuff/types';
import * as v from 'valibot';

export const getprofile = query(
	v.object({
		steam64: v.string(),
		recall: v.number()
	}),
	async (data) => {
		let profile = {} as Userdetails;
		// console.log(profile)
		let status = 500
		try {
			 const response = await fetch(`${API_URL}/profile`, {
				method: 'POST',
				body: JSON.stringify({ url: data.steam64, expand: true, timeout: data.recall }),
				headers: { 'Content-Type': 'application/json' }
			});

			if (response.ok) {
				profile = await response.json();
			}
			status = response.status
		} catch {
			
		}

		return { profile, statuscode: status };
	}
);


export const getwordcloud = query(
	v.string(),
	async (steam64) => {
		let status = 500;

		try {
			const response = await fetch(`${API_URL}/wordcloud/${encodeURIComponent(steam64)}`, {
				method: 'GET'
			});

			status = response.status;

			if (!response.ok) {
				return { profile: '', statuscode: status };
			}

			const contentType = response.headers.get('content-type') ?? 'image/png';
			const bytes = new Uint8Array(await response.arrayBuffer());
			let binary = '';

			for (const byte of bytes) {
				binary += String.fromCharCode(byte);
			}

			return { profile: `data:${contentType};base64,${btoa(binary)}`, statuscode: status };
		} catch {
			return { profile: '', statuscode: status };
		}
	}
);
