
export default (pageContext: { urlPathname: string }) => {
  const path = pageContext.urlPathname
  if (path === '/' || path === '') return false
  const match = path.match(/^\/(.+)$/)
  if (match) {
    return {
      routeParams: {
        userid: match[1]
      }
    }
  }

  return false
}
