import { writable } from 'svelte/store';

export function mousePosition(init = {x: 0, y: 0}) {
	if (!window) return writable(init);
	
	const store = writable(
		init,
		() => () => window.removeEventListener('mousemove', updatePosition)
	)
	
	function updatePosition(e: MouseEvent) {
		store.set({ x: e.clientX, y: e.clientY });
	}
	
	window.addEventListener('mousemove', updatePosition)
	
	return {
		subscribe: store.subscribe
	}
}
