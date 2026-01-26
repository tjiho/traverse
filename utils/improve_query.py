def improve_query(query: str) -> str:
  if len(query.split()) == 1:
    return f"{query} {query} {query}"
  return query