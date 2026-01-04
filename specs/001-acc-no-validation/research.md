# Research: Acc No Uniqueness Validation

## Decision: Use EXISTS instead of COUNT for duplicate checking
**Rationale**: PostgreSQL's EXISTS operator is more efficient than COUNT for checking if a record exists because it returns as soon as the first matching row is found, whereas COUNT must scan all matching rows. For duplicate checking, we only need to know if at least one record exists, not how many.

**Alternatives considered**:
- COUNT(*) - less efficient as it counts all matching records
- SELECT 1 FROM table WHERE condition LIMIT 1 - similar performance to EXISTS but EXISTS is more semantically appropriate

## Decision: Use Python sets for bulk validation lookups
**Rationale**: Python sets provide O(1) average time complexity for membership testing, making them ideal for checking if acc_no values exist in the database results. This is much more efficient than searching through lists for each validation.

**Alternatives considered**:
- Lists - O(n) lookup time
- Dictionaries - O(1) but use more memory with key-value pairs when we only need keys

## Decision: Use pandas duplicated() method for internal duplicate detection
**Rationale**: Pandas DataFrame.duplicated() method is specifically designed to identify duplicate rows efficiently. It can operate on specific columns and offers flexibility with the 'keep' parameter to control which duplicates to mark.

**Alternatives considered**:
- Manual iteration - less efficient and more error-prone
- Using groupby - more complex for simple duplicate detection

## Decision: Use pandas isin() method for filtering valid records
**Rationale**: DataFrame.isin() is optimized for membership testing against a collection of values. It's efficient for filtering out records with acc_no values that already exist in the database.

**Alternatives considered**:
- Manual iteration with apply - much slower
- Query method - less flexible for complex conditions

## Decision: Use Streamlit session state for form preservation
**Rationale**: Streamlit's session_state mechanism allows preserving form data across reruns, which is essential when validation fails and we want to keep user input intact.

**Alternatives considered**:
- Page reload with URL parameters - not suitable for sensitive data
- Client-side storage - not persistent across sessions

## Decision: Use PostgreSQL B-tree index on acc_no columns
**Rationale**: B-tree indexes provide efficient equality and range queries, which is perfect for acc_no lookups. Creating an index on the acc_no columns will significantly improve the performance of duplicate checks.

**Alternatives considered**:
- No index - queries would be slow on large datasets
- Hash index - not appropriate for range queries and has limitations