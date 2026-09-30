# F5 pilot: items

60 items, Q01 to Q60. `items.json` holds the same content in machine-readable form.

## Phase 1 lists

Forecast items, grouped into three triage blocks of 15. In each block you will choose exactly 5.

- **Block A:** Q01, Q12, Q14, Q18, Q19, Q27, Q30, Q31, Q34, Q36, Q48, Q50, Q51, Q54, Q57
- **Block B:** Q02, Q05, Q07, Q16, Q20, Q22, Q28, Q33, Q35, Q40, Q42, Q44, Q47, Q49, Q53
- **Block C:** Q03, Q04, Q17, Q21, Q23, Q24, Q25, Q32, Q37, Q39, Q46, Q52, Q58, Q59, Q60

Items that appear in no block are not forecast in Phase 1. Every item (all 60) is attempted in Phase 2.

---

## Q01 · family: program-output

Predict exactly what this Python 3 program prints.

```python
stack = []
out = []
for x in [7, 2, 6, 7, 5, 3, 8, 8, 9, 9, 8, 1, 6]:
    if stack and (stack[-1] + x) % 3 == 0:
        out.append(stack.pop() * x)
    else:
        stack.append(x)
print(out, stack)
```

**Answer format:** exactly the one line the program prints

---

## Q02 · family: stock-log

Read this stock log and answer the question.

Rules for reading the log:
- Every entry is an accurate record, except that a CORRECTION replaces the quantity stated in the entry it names (the correction applies wherever it appears in the log).
- Stock changes only through the deliveries, shipments and transfers recorded here.
- Entries are in time order. A stocktake states the exact stock at the end of that day.

Opening stock (start of Day 1): Canal Store: 19 crates of salt, 11 crates of flour; Harbor Shed: 27 crates of salt, 55 crates of flour.

#1 Day 1: a delivery of salt arrived at Canal Store; the number of crates was not recorded.
#2 Day 1: 22 crates of flour delivered to Harbor Shed.
#3 Day 1: an inspector visited Canal Store; no goods moved.
#4 Day 2: 24 crates of salt delivered to Harbor Shed.
#5 Day 2: 10 crates of flour moved from Canal Store to Harbor Shed.
#6 Day 2: 52 crates of flour shipped out from Harbor Shed.
#7 Day 3: 10 crates of salt delivered to Harbor Shed.
#8 Day 3: 16 crates of salt delivered to Canal Store.
#9 Day 3: stocktake: Canal Store holds 42 crates of salt.
#10 Day 4: 23 crates of salt delivered to Canal Store.
#11 Day 4: 18 crates of salt delivered to Harbor Shed.
#12 Day 5: 11 crates of flour delivered to Canal Store.
#13 Day 5: 5 crates of salt delivered to Harbor Shed.
#14 Day 5: a delivery of salt arrived at Harbor Shed; the number of crates was not recorded.
#15 Day 5: stocktake: Harbor Shed holds 35 crates of flour.
#16 Day 6: the loading crane at Harbor Shed was repaired.
#17 Day 6: 39 crates of flour delivered to Harbor Shed.
#18 Day 7: 8 crates of flour moved from Canal Store to Harbor Shed.
#19 Day 7: 15 crates of salt delivered to Canal Store.
#20 Day 7: CORRECTION to entry #19: the quantity was 26 crates, not 15 crates.
#21 Day 7: 3 crates of salt shipped out from Harbor Shed.
#22 Day 7: stocktake: Canal Store holds 4 crates of flour.

Question: how many crates of salt were in Harbor Shed at the end of Day 5?
Answer with a whole number of crates; or CONTRADICTORY if statements in the log that bear on this number cannot all be true; or NOT DETERMINABLE if the log does not contain enough information to fix the number.

**Answer format:** a whole number, or CONTRADICTORY, or NOT DETERMINABLE

---

## Q03 · family: string-trace

A rewriting process starts from the string CBBA and uses these rules:
Rule 1: AC → CBB
Rule 2: B → ACB
Rule 3: A → (empty string)

One step: find the lowest-numbered rule whose left-hand side occurs somewhere in the current string, and replace the leftmost occurrence of that left-hand side with the rule's right-hand side. (Only one replacement is made per step.)

Question: what is the string after exactly 3 steps?

**Answer format:** the resulting string (letters only)

---

## Q04 · family: program-output

Predict exactly what this Python 3 program prints.

```python
n = 204
steps = 0
peak = n
while n >= 10:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    peak = max(peak, n)
    steps += 1
print(steps, peak, n)
```

**Answer format:** exactly the one line the program prints

---

## Q05 · family: stock-log

Read this stock log and answer the question.

Rules for reading the log:
- Every entry is an accurate record, except that a CORRECTION replaces the quantity stated in the entry it names (the correction applies wherever it appears in the log).
- Stock changes only through the deliveries, shipments and transfers recorded here.
- Entries are in time order. A stocktake states the exact stock at the end of that day.

Opening stock (start of Day 1): Canal Store: 7 crates of rope, 47 crates of soap; Mill Loft: 59 crates of rope, 51 crates of soap.

#1 Day 1: 10 crates of rope delivered to Canal Store.
#2 Day 1: 14 crates of rope moved from Canal Store to Mill Loft.
#3 Day 2: 29 crates of soap moved from Mill Loft to Canal Store.
#4 Day 2: 5 crates of soap delivered to Mill Loft.
#5 Day 3: 18 crates of rope delivered to Mill Loft.
#6 Day 3: 3 crates of rope delivered to Mill Loft.
#7 Day 3: stocktake: Mill Loft holds 94 crates of rope.
#8 Day 3: stocktake: Canal Store holds 76 crates of soap.
#9 Day 4: a delivery of rope arrived at Mill Loft; the number of crates was not recorded.
#10 Day 4: 16 crates of soap delivered to Canal Store.
#11 Day 4: 23 crates of soap moved from Mill Loft to Canal Store.
#12 Day 4: 28 crates of soap delivered to Mill Loft.
#13 Day 5: 28 crates of soap moved from Mill Loft to Canal Store.
#14 Day 5: an inspector visited Mill Loft; no goods moved.
#15 Day 6: 96 crates of rope moved from Mill Loft to Canal Store.
#16 Day 6: 7 crates of rope delivered to Mill Loft.

Question: how many crates of rope were in Mill Loft at the end of Day 4?
Answer with a whole number of crates; or CONTRADICTORY if statements in the log that bear on this number cannot all be true; or NOT DETERMINABLE if the log does not contain enough information to fix the number.

**Answer format:** a whole number, or CONTRADICTORY, or NOT DETERMINABLE

---

## Q06 · family: rule-inference

Each line below shows an input list of integers and the output list that a hidden rule produces from it. The same rule is used on every line.
[1, 0, 5, 6, 6, 3] → [5, 6, 6, 3, 1, 0]
[10, 10, 5, 5, 4, 12] → [5, 5, 4, 12, 10, 10]
[6, 8, 8, 0, 2, 4, 11, 9] → [8, 0, 2, 4, 11, 9, 6, 8]
[8, 10, 12, 12, 5, 10, 7] → [12, 12, 5, 10, 7, 8, 10]
[1, 4, 1, 0, 4, 3] → [1, 0, 4, 3, 1, 4]

Question: what output does the rule produce for the input [6, 7, 6, 1, 9, 2, 0, 4]?

**Answer format:** a list of integers in square brackets

---

## Q07 · family: stock-log

Read this stock log and answer the question.

Rules for reading the log:
- Every entry is an accurate record, except that a CORRECTION replaces the quantity stated in the entry it names (the correction applies wherever it appears in the log).
- Stock changes only through the deliveries, shipments and transfers recorded here.
- Entries are in time order. A stocktake states the exact stock at the end of that day.
- Harbor Shed is also referred to as Unit 12.

Opening stock (start of Day 1): Canal Store: 13 crates of flour, 30 crates of salt, 10 crates of soap; Harbor Shed: 24 crates of flour, 45 crates of salt, 7 crates of soap; Mill Loft: 44 crates of flour, 41 crates of salt, 33 crates of soap.

#1 Day 1: 3 crates of flour moved from Canal Store to Harbor Shed.
#2 Day 1: 4 crates of flour delivered to Unit 12.
#3 Day 1: 20 crates of soap delivered to Harbor Shed.
#4 Day 1: 24 crates of flour delivered to Mill Loft.
#5 Day 2: 34 crates of flour delivered to Mill Loft.
#6 Day 2: 16 crates of salt delivered to Harbor Shed.
#7 Day 2: 27 crates of salt moved from Canal Store to Mill Loft.
#8 Day 2: stocktake: Unit 12 holds 31 crates of flour.
#9 Day 3: 33 crates of salt moved from Mill Loft to Canal Store.
#10 Day 3: a delivery of salt arrived at Canal Store; the number of crates was not recorded.
#11 Day 3: 7 crates of flour delivered to Harbor Shed.
#12 Day 3: 20 crates of soap delivered to Mill Loft.
#13 Day 3: 6 crates of flour moved from Unit 12 to Mill Loft.
#14 Day 4: the gate lock at Unit 12 was replaced.
#15 Day 4: 1 crate of flour shipped out from Canal Store.
#16 Day 4: CORRECTION to entry #11: the quantity was 14 crates, not 7 crates.
#17 Day 4: 12 crates of soap shipped out from Mill Loft.
#18 Day 4: 31 crates of soap delivered to Harbor Shed.
#19 Day 5: 25 crates of salt delivered to Mill Loft.
#20 Day 5: 5 crates of salt moved from Canal Store to Harbor Shed.
#21 Day 5: stocktake: Mill Loft holds 41 crates of soap.
#22 Day 6: 37 crates of flour delivered to Harbor Shed.
#23 Day 6: 21 crates of salt shipped out from Mill Loft.
#24 Day 6: a delivery of salt arrived at Canal Store; the number of crates was not recorded.
#25 Day 6: stocktake: Harbor Shed holds 66 crates of salt.
#26 Day 7: the loading crane at Harbor Shed was repaired.
#27 Day 7: Canal Store was closed for half a day for cleaning.
#28 Day 7: the gate lock at Canal Store was replaced.
#29 Day 8: 31 crates of salt delivered to Canal Store.
#30 Day 8: 15 crates of salt moved from Unit 12 to Canal Store.
#31 Day 8: 60 crates of salt delivered to Canal Store.
#32 Day 8: 50 crates of salt shipped out from Harbor Shed.
#33 Day 8: CORRECTION to entry #31: the quantity was 40 crates, not 60 crates.
#34 Day 8: stocktake: Canal Store holds 10 crates of soap.

Question: how many crates of flour were in Mill Loft at the end of Day 5?
Answer with a whole number of crates; or CONTRADICTORY if statements in the log that bear on this number cannot all be true; or NOT DETERMINABLE if the log does not contain enough information to fix the number.

**Answer format:** a whole number, or CONTRADICTORY, or NOT DETERMINABLE

---

## Q08 · family: string-trace

A rewriting process starts from the string CCABCCB and uses these rules:
Rule 1: CC → C
Rule 2: CA → A
Rule 3: C → BC
Rule 4: B → A

One step: find the lowest-numbered rule whose left-hand side occurs somewhere in the current string, and replace the leftmost occurrence of that left-hand side with the rule's right-hand side. (Only one replacement is made per step.)

Question: what is the string after exactly 10 steps?

**Answer format:** the resulting string (letters only)

---

## Q09 · family: program-output

Predict exactly what this Python 3 program prints.

```python
word = "fazujmki"
out = ""
for ch in word:
    if ch in "aeiou":
        out = ch + out
    else:
        out = out + ch
print(out)
```

**Answer format:** exactly the one line the program prints

---

## Q10 · family: stock-log

Read this stock log and answer the question.

Rules for reading the log:
- Every entry is an accurate record, except that a CORRECTION replaces the quantity stated in the entry it names (the correction applies wherever it appears in the log).
- Stock changes only through the deliveries, shipments and transfers recorded here.
- Entries are in time order. A stocktake states the exact stock at the end of that day.

Opening stock (start of Day 1): North Yard: 25 crates of tea, 16 crates of flour; Harbor Shed: 18 crates of tea, 18 crates of flour.

#1 Day 1: 24 crates of tea delivered to Harbor Shed.
#2 Day 1: 26 crates of tea delivered to Harbor Shed.
#3 Day 1: 8 crates of flour moved from North Yard to Harbor Shed.
#4 Day 1: stocktake: North Yard holds 25 crates of tea.
#5 Day 2: 16 crates of tea delivered to Harbor Shed.
#6 Day 3: the gate lock at Harbor Shed was replaced.
#7 Day 3: stocktake: Harbor Shed holds 22 crates of flour.
#8 Day 4: 4 crates of tea delivered to Harbor Shed.
#9 Day 5: 4 crates of flour moved from North Yard to Harbor Shed.
#10 Day 6: 3 crates of flour shipped out from North Yard.
#11 Day 6: 19 crates of flour moved from Harbor Shed to North Yard.
#12 Day 6: a delivery of flour arrived at Harbor Shed; the number of crates was not recorded.
#13 Day 6: 9 crates of tea moved from North Yard to Harbor Shed.

Question: how many crates of flour were in Harbor Shed at the end of Day 3?
Answer with a whole number of crates; or CONTRADICTORY if statements in the log that bear on this number cannot all be true; or NOT DETERMINABLE if the log does not contain enough information to fix the number.

**Answer format:** a whole number, or CONTRADICTORY, or NOT DETERMINABLE

---

## Q11 · family: logic-grid

3 people live in a row of 3 houses, numbered 1 to 3 from left to right. Each person has a different name and a different pet. The possible values are: names: Ada, Dov, Hana; pets: hare, newt, owl. "Directly to the left of" means in the house numbered one lower; "next to" means in an adjacent house.

Clues:
1. Dov lives directly to the left of the hare owner.
2. Hana lives in house 2.
3. The hare owner lives next to Ada.
4. The hare owner is not Dov.
5. Ada does not own the hare.
6. Ada owns the owl.
7. Ada lives next to the hare owner.

Question: list the names in house order, from house 1 to house 3.

**Answer format:** the 3 names separated by commas, in house order 1 to 3

---

## Q12 · family: program-output

Predict exactly what this Python 3 program prints.

```python
a = list(range(1, 11 + 1))
for k in range(2, 5):
    for i in range(0, len(a), k):
        a[i], a[-1 - i] = a[-1 - i], a[i]
    a = a[1:] + a[:1]
print(a)
```

**Answer format:** exactly the one line the program prints

---

## Q13 · family: stock-log

Read this stock log and answer the question.

Rules for reading the log:
- Every entry is an accurate record, except that a CORRECTION replaces the quantity stated in the entry it names (the correction applies wherever it appears in the log).
- Stock changes only through the deliveries, shipments and transfers recorded here.
- Entries are in time order. A stocktake states the exact stock at the end of that day.

Opening stock (start of Day 1): Harbor Shed: 31 crates of soap, 37 crates of salt; Canal Store: 49 crates of soap, 56 crates of salt.

#1 Day 1: 18 crates of salt moved from Harbor Shed to Canal Store.
#2 Day 1: 8 crates of salt moved from Harbor Shed to Canal Store.
#3 Day 1: 14 crates of soap moved from Harbor Shed to Canal Store.
#4 Day 2: 33 crates of salt delivered to Harbor Shed.
#5 Day 2: 34 crates of salt delivered to Harbor Shed.
#6 Day 2: 5 crates of salt delivered to Canal Store.
#7 Day 2: a delivery of salt arrived at Harbor Shed; the number of crates was not recorded.
#8 Day 2: stocktake: Canal Store holds 87 crates of salt.
#9 Day 2: stocktake: Harbor Shed holds 86 crates of salt.
#10 Day 3: 9 crates of soap delivered to Canal Store.
#11 Day 3: the gate lock at Canal Store was replaced.
#12 Day 4: 22 crates of soap delivered to Harbor Shed.
#13 Day 4: the loading crane at Canal Store was repaired.
#14 Day 4: a delivery of salt arrived at Harbor Shed; the number of crates was not recorded.
#15 Day 5: 35 crates of soap shipped out from Harbor Shed.
#16 Day 5: 3 crates of soap moved from Harbor Shed to Canal Store.
#17 Day 6: 19 crates of salt delivered to Canal Store.
#18 Day 6: 58 crates of soap moved from Canal Store to Harbor Shed.
#19 Day 6: stocktake: Harbor Shed holds 57 crates of soap.
#20 Day 7: 35 crates of salt moved from Harbor Shed to Canal Store.
#21 Day 7: 56 crates of salt shipped out from Canal Store.
#22 Day 7: CORRECTION to entry #12: the quantity was 32 crates, not 22 crates.

Question: how many crates of soap were in Harbor Shed at the end of Day 6?
Answer with a whole number of crates; or CONTRADICTORY if statements in the log that bear on this number cannot all be true; or NOT DETERMINABLE if the log does not contain enough information to fix the number.

**Answer format:** a whole number, or CONTRADICTORY, or NOT DETERMINABLE

---

## Q14 · family: stock-log

Read this stock log and answer the question.

Rules for reading the log:
- Every entry is an accurate record, except that a CORRECTION replaces the quantity stated in the entry it names (the correction applies wherever it appears in the log).
- Stock changes only through the deliveries, shipments and transfers recorded here.
- Entries are in time order. A stocktake states the exact stock at the end of that day.
- One pallet holds exactly 12 crates.
- North Yard is also referred to as Unit 12.

Opening stock (start of Day 1): Mill Loft: 15 crates of lamp oil, 0 crates of soap, 15 crates of copper wire; North Yard: 9 crates of lamp oil, 54 crates of soap, 28 crates of copper wire; Canal Store: 0 crates of lamp oil, 53 crates of soap, 46 crates of copper wire.

#1 Day 1: 35 crates of lamp oil delivered to Canal Store.
#2 Day 1: 25 crates of soap shipped out from North Yard.
#3 Day 1: 11 crates of lamp oil moved from Mill Loft to North Yard.
#4 Day 1: the loading crane at Mill Loft was repaired.
#5 Day 2: 14 crates of copper wire delivered to Unit 12.
#6 Day 2: Mill Loft was closed for half a day for cleaning.
#7 Day 2: 11 crates of lamp oil moved from Unit 12 to Canal Store.
#8 Day 3: 26 crates of soap delivered to North Yard.
#9 Day 3: 7 crates of copper wire moved from Mill Loft to Canal Store.
#10 Day 3: 20 crates of lamp oil delivered to Mill Loft.
#11 Day 3: 14 crates of soap delivered to Mill Loft.
#12 Day 4: 1 pallet of soap delivered to Canal Store.
#13 Day 4: 4 pallets of lamp oil delivered to Mill Loft.
#14 Day 4: 36 crates of copper wire delivered to Mill Loft.
#15 Day 4: a delivery of lamp oil arrived at Canal Store; the number of crates was not recorded.
#16 Day 4: 31 crates of copper wire shipped out from North Yard.
#17 Day 4: stocktake: Unit 12 holds 55 crates of soap.
#18 Day 5: 38 crates of lamp oil moved from Canal Store to North Yard.
#19 Day 5: 34 crates of lamp oil shipped out from Mill Loft.
#20 Day 5: 34 crates of lamp oil delivered to North Yard.
#21 Day 6: 37 crates of copper wire moved from Mill Loft to Canal Store.
#22 Day 6: 6 crates of lamp oil delivered to Unit 12.
#23 Day 6: 56 crates of lamp oil delivered to Canal Store.
#24 Day 7: 3 pallets of lamp oil delivered to North Yard.
#25 Day 7: 28 crates of soap delivered to North Yard.
#26 Day 7: an inspector visited Mill Loft; no goods moved.
#27 Day 7: 6 crates of soap moved from Mill Loft to Canal Store.
#28 Day 7: stocktake: Canal Store holds 83 crates of soap.
#29 Day 8: the loading crane at Mill Loft was repaired.
#30 Day 8: 23 crates of soap shipped out from North Yard.
#31 Day 8: CORRECTION to entry #12: the quantity was 2 pallets, not 1 pallet.
#32 Day 8: 4 pallets of lamp oil delivered to Canal Store.
#33 Day 8: 17 crates of lamp oil delivered to North Yard.
#34 Day 8: stocktake: Mill Loft holds 3 crates of copper wire.
#35 Day 8: stocktake: Unit 12 holds 11 crates of copper wire.
#36 Day 9: 21 crates of lamp oil delivered to Mill Loft.
#37 Day 9: a delivery of soap arrived at Unit 12; the number of crates was not recorded.
#38 Day 9: 113 crates of lamp oil moved from Canal Store to Mill Loft.
#39 Day 9: 29 crates of soap delivered to North Yard.
#40 Day 9: 4 pallets of copper wire delivered to Mill Loft.
#41 Day 9: CORRECTION to entry #23: the quantity was 38 crates, not 56 crates.
#42 Day 9: stocktake: Mill Loft holds 172 crates of lamp oil.

Question: how many crates of copper wire were in Mill Loft at the end of Day 8?
Answer with a whole number of crates; or CONTRADICTORY if statements in the log that bear on this number cannot all be true; or NOT DETERMINABLE if the log does not contain enough information to fix the number.

**Answer format:** a whole number, or CONTRADICTORY, or NOT DETERMINABLE

---

## Q15 · family: exact-computation

Compute 25334 × 4367.

**Answer format:** a single integer (digits only)

---

## Q16 · family: program-output

Predict exactly what this Python 3 program prints.

```python
cells = [1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0]
for step in range(5):
    cells = [cells[i - 1] ^ cells[(i + 1) % 11] ^ (cells[i] & cells[i - 1]) for i in range(11)]
print("".join(str(c) for c in cells))
```

**Answer format:** exactly the one line the program prints

---

## Q17 · family: logic-grid

5 people live in a row of 5 houses, numbered 1 to 5 from left to right. Each person has a different name, a different drink, a different pet and a house of a different colour. The possible values are: names: Bram, Cleo, Dov, Esme, Fitz; drinks: cider, cocoa, coffee, kefir, water; pets: crow, dog, goat, hare, newt; colours: blue, grey, red, white, yellow. "Directly to the left of" means in the house numbered one lower; "next to" means in an adjacent house.

Clues:
1. Bram does not live next to the cocoa drinker.
2. The dog owner does not live in house 1.
3. The resident of the blue house owns the newt.
4. The water drinker lives in one of the two end houses.
5. The resident of the grey house does not live next to the resident of the yellow house.
6. Bram lives next to the resident of the red house.
7. Cleo lives next to the cocoa drinker.
8. The kefir drinker is not Dov.
9. The hare owner does not live in house 3.
10. The resident of the grey house lives somewhere to the left of the kefir drinker.
11. The resident of the white house lives somewhere to the left of the newt owner.
12. Esme owns the dog.
13. The hare owner does not live in house 1.
14. The kefir drinker lives next to the cider drinker.
15. The coffee drinker lives somewhere to the left of the cocoa drinker.
16. The kefir drinker does not live next to the hare owner.
17. The resident of the grey house lives directly to the left of the goat owner.
18. The kefir drinker lives in one of the two end houses.
19. The dog owner does not live next to Cleo.
20. Bram does not live in house 5.

Question: list the names in house order, from house 1 to house 5.

**Answer format:** the 5 names separated by commas, in house order 1 to 5

---

## Q18 · family: string-trace

Start with the string ewhsa. Apply the following operations in order. Positions are numbered from 1 at the left. Rotating left by one step moves the first letter to the end; rotating right by one step moves the last letter to the front.
1. Rotate left by 3 steps.
2. Reverse the letters in positions 1 through 2.
3. Reverse the letters in positions 2 through 3.

Question: what is the final string?

**Answer format:** the final string (letters only)

---

## Q19 · family: rule-inference

Each line below shows an input list of integers and the output list that a hidden rule produces from it. The same rule is used on every line.
[5, 6, 5, 3, 5, 4, 3] → [11, 12, 12, 12, 12, 12, 11]
[4, 5, 3, 11, 4, 6, 12, 6] → [9, 10, 16, 22, 22, 23, 24, 16]
[4, 6, 10, 9, 2, 12, 3] → [10, 16, 20, 20, 22, 24, 16]
[8, 4, 10, 0, 8, 6, 0] → [16, 18, 20, 20, 20, 20, 18]
[8, 6, 6, 5, 8, 4, 5] → [16, 16, 16, 16, 16, 16, 16]
[9, 0, 9, 0, 4, 4, 9] → [18, 18, 18, 18, 18, 18, 18]

Question: what output does the rule produce for the input [0, 7, 3, 2, 0]?

**Answer format:** a list of integers in square brackets

---

## Q20 · family: string-trace

Start with the string ovzefldj. Apply the following operations in order. Positions are numbered from 1 at the left. Rotating left by one step moves the first letter to the end; rotating right by one step moves the last letter to the front.
1. Swap the letters in positions 6 and 8.
2. Reverse the letters in positions 2 through 6.
3. Swap the letters l and z (wherever they currently are).
4. Reverse the letters in positions 2 through 6.
5. Reverse the letters in positions 5 through 6.
6. Remove the letter in position 2 and reinsert it so that it ends up in position 6.
7. Rotate left by 3 steps.
8. Remove the letter in position 3 and reinsert it so that it ends up in position 8.
9. Rotate right by 3 steps.
10. Reverse the letters in positions 2 through 8.

Question: what is the final string?

**Answer format:** the final string (letters only)

---

## Q21 · family: stock-log

Read this stock log and answer the question.

Rules for reading the log:
- Every entry is an accurate record, except that a CORRECTION replaces the quantity stated in the entry it names (the correction applies wherever it appears in the log).
- Stock changes only through the deliveries, shipments and transfers recorded here.
- Entries are in time order. A stocktake states the exact stock at the end of that day.
- Mill Loft is also referred to as Unit 12.

Opening stock (start of Day 1): Canal Store: 6 crates of tea, 43 crates of salt, 57 crates of copper wire; Mill Loft: 32 crates of tea, 58 crates of salt, 17 crates of copper wire; East Depot: 35 crates of tea, 7 crates of salt, 23 crates of copper wire.

#1 Day 1: 2 crates of copper wire shipped out from Canal Store.
#2 Day 1: 2 crates of tea moved from Canal Store to Unit 12.
#3 Day 2: 58 crates of salt shipped out from Unit 12.
#4 Day 2: 7 crates of salt shipped out from Mill Loft.
#5 Day 2: 1 crate of salt shipped out from East Depot.
#6 Day 2: stocktake: East Depot holds 35 crates of tea.
#7 Day 3: 6 crates of tea moved from Unit 12 to East Depot.
#8 Day 3: 5 crates of salt delivered to East Depot.
#9 Day 4: a delivery of salt arrived at Unit 12; the number of crates was not recorded.
#10 Day 4: 15 crates of copper wire delivered to Unit 12.
#11 Day 4: a delivery of tea arrived at Canal Store; the number of crates was not recorded.
#12 Day 4: 6 crates of salt delivered to Mill Loft.
#13 Day 4: stocktake: Canal Store holds 43 crates of salt.
#14 Day 5: 8 crates of tea shipped out from Canal Store.
#15 Day 5: 6 crates of copper wire delivered to Mill Loft.
#16 Day 5: 8 crates of salt moved from Canal Store to East Depot.
#17 Day 5: 30 crates of copper wire delivered to East Depot.
#18 Day 6: Canal Store was closed for half a day for cleaning.
#19 Day 6: 45 crates of copper wire moved from Canal Store to Mill Loft.
#20 Day 6: 11 crates of tea delivered to Canal Store.
#21 Day 6: 1 crate of salt moved from East Depot to Mill Loft.
#22 Day 7: 30 crates of copper wire moved from East Depot to Canal Store.
#23 Day 7: 27 crates of copper wire moved from East Depot to Canal Store.
#24 Day 7: CORRECTION to entry #23: the quantity was 21 crates, not 27 crates.
#25 Day 7: stocktake: East Depot holds 41 crates of tea.
#26 Day 8: 38 crates of salt delivered to Unit 12.
#27 Day 8: CORRECTION to entry #3: the quantity was 49 crates, not 58 crates.
#28 Day 8: 14 crates of tea moved from East Depot to Canal Store.
#29 Day 8: 13 crates of copper wire shipped out from Canal Store.
#30 Day 8: 18 crates of copper wire delivered to Mill Loft.
#31 Day 8: stocktake: Mill Loft holds 28 crates of tea.

Question: how many crates of salt were in Mill Loft at the end of Day 5?
Answer with a whole number of crates; or CONTRADICTORY if statements in the log that bear on this number cannot all be true; or NOT DETERMINABLE if the log does not contain enough information to fix the number.

**Answer format:** a whole number, or CONTRADICTORY, or NOT DETERMINABLE

---

## Q22 · family: program-output

Predict exactly what this Python 3 program prints.

```python
a, b, c = 18, 6, 2
while a > 0:
    if (a + b) % 3 == 0:
        b = b * 2 - c
        a = a - 2
    elif b % 3 == 0:
        c = c + a
        a = a - 1
    else:
        b = b + 2
        c = c - 1
        a = a - 1
print(a, b, c)
```

**Answer format:** exactly the one line the program prints

---

## Q23 · family: rule-inference

Each line below shows an input list of integers and the output list that a hidden rule produces from it. The same rule is used on every line.
[1, 0, 11, 9, 11] → [1, 0, 11, 9]
[1, 3, 1, 3, 1, 8, 3, 10] → [1, 3, 1, 3, 1, 8, 3]
[0, 8, 1, 9, 4, 2, 6, 5] → [0, 8, 1, 9, 4, 2, 6]
[5, 9, 12, 5, 5, 7, 7] → [5, 9, 12, 5, 5, 7]
[9, 3, 4, 12, 10, 0, 11, 0] → [9, 3, 4, 12, 10, 0, 11]

Question: what output does the rule produce for the input [10, 7, 1, 1, 6]?

**Answer format:** a list of integers in square brackets

---

## Q24 · family: rule-inference

Each line below shows an input list of integers and the output list that a hidden rule produces from it. The same rule is used on every line.
[6, 6, 9, 9, 12, 3, 7, 0] → [0, 3, 0, -6, 9, -12, 7]
[8, 11, 2, 4, 0, 1, 0, 5] → [-3, -4, -2, -1, -1, 5, -5]
[10, 1, 11, 11, 12, 8, 8] → [9, 1, 0, -3, 4, -4]
[0, 1, 10, 6, 4] → [-1, 6, 4, -6]
[7, 12, 0, 3, 11, 5, 10] → [-5, -4, -3, 5, 6, -1]
[9, 5, 2, 7, 9, 12, 5] → [4, -2, -5, 10, -3, -4]

Question: what output does the rule produce for the input [5, 9, 9, 2, 0, 7, 4]?

**Answer format:** a list of integers in square brackets

---

## Q25 · family: stock-log

Read this stock log and answer the question.

Rules for reading the log:
- Every entry is an accurate record, except that a CORRECTION replaces the quantity stated in the entry it names (the correction applies wherever it appears in the log).
- Stock changes only through the deliveries, shipments and transfers recorded here.
- Entries are in time order. A stocktake states the exact stock at the end of that day.
- One pallet holds exactly 12 crates.
- East Depot is also referred to as Store B.

Opening stock (start of Day 1): Harbor Shed: 25 crates of rope, 24 crates of salt, 11 crates of soap; Bell Barn: 29 crates of rope, 24 crates of salt, 5 crates of soap; East Depot: 39 crates of rope, 40 crates of salt, 52 crates of soap.

#1 Day 1: 35 crates of rope delivered to Bell Barn.
#2 Day 1: 39 crates of soap delivered to Harbor Shed.
#3 Day 1: 40 crates of soap delivered to Bell Barn.
#4 Day 1: 9 crates of salt delivered to Store B.
#5 Day 2: the gate lock at Bell Barn was replaced.
#6 Day 2: 10 crates of rope moved from East Depot to Bell Barn.
#7 Day 2: 10 crates of salt shipped out from Harbor Shed.
#8 Day 2: stocktake: East Depot holds 29 crates of rope.
#9 Day 3: a delivery of salt arrived at Harbor Shed; the number of crates was not recorded.
#10 Day 3: 22 crates of soap moved from Harbor Shed to East Depot.
#11 Day 3: 2 pallets of salt delivered to Harbor Shed.
#12 Day 3: 16 crates of salt moved from Bell Barn to Harbor Shed.
#13 Day 3: 16 crates of soap delivered to Bell Barn.
#14 Day 3: stocktake: Store B holds 29 crates of rope.
#15 Day 4: 1 crate of soap shipped out from Harbor Shed.
#16 Day 4: the loading crane at East Depot was repaired.
#17 Day 4: 18 crates of rope moved from Bell Barn to East Depot.
#18 Day 4: stocktake: Bell Barn holds 8 crates of salt.
#19 Day 5: a delivery of soap arrived at Harbor Shed; the number of crates was not recorded.
#20 Day 5: 1 pallet of salt delivered to Harbor Shed.
#21 Day 5: 1 pallet of salt delivered to Harbor Shed.
#22 Day 5: the gate lock at Bell Barn was replaced.
#23 Day 5: stocktake: Bell Barn holds 56 crates of rope.
#24 Day 6: 3 pallets of rope delivered to Bell Barn.
#25 Day 6: the loading crane at Harbor Shed was repaired.
#26 Day 6: 13 crates of rope delivered to Bell Barn.
#27 Day 7: 2 pallets of rope delivered to Bell Barn.
#28 Day 7: CORRECTION to entry #26: the quantity was 17 crates, not 13 crates.
#29 Day 7: 17 crates of soap delivered to Bell Barn.
#30 Day 7: the loading crane at Store B was repaired.
#31 Day 7: 4 pallets of salt delivered to Store B.
#32 Day 8: 34 crates of rope moved from Bell Barn to East Depot.
#33 Day 8: 24 crates of rope delivered to East Depot.
#34 Day 8: an inspector visited Store B; no goods moved.
#35 Day 8: stocktake: Harbor Shed holds 41 crates of soap.
#36 Day 9: 44 crates of soap moved from East Depot to Bell Barn.
#37 Day 9: 67 crates of salt moved from Store B to Harbor Shed.
#38 Day 9: 10 crates of soap shipped out from Bell Barn.
#39 Day 9: CORRECTION to entry #38: the quantity was 7 crates, not 10 crates.

Question: how many crates of rope were in Harbor Shed at the end of Day 5?
Answer with a whole number of crates; or CONTRADICTORY if statements in the log that bear on this number cannot all be true; or NOT DETERMINABLE if the log does not contain enough information to fix the number.

**Answer format:** a whole number, or CONTRADICTORY, or NOT DETERMINABLE

---

## Q26 · family: exact-computation

Compute 311 × 863.

**Answer format:** a single integer (digits only)

---

## Q27 · family: program-output

Predict exactly what this Python 3 program prints.

```python
x = 23
queue = []
score = 0
for t in range(17):
    x = (22 * x + 12) % 97
    if x % 3 == 0:
        queue.append(x)
    elif queue:
        score += queue.pop(0) * (t % 4 + 1)
    else:
        score -= 1
print(score, len(queue), x)
```

**Answer format:** exactly the one line the program prints

---

## Q28 · family: logic-grid

4 people live in a row of 4 houses, numbered 1 to 4 from left to right. Each person has a different name, a different pet and a different drink. The possible values are: names: Ada, Bram, Dov, Fitz; pets: cat, dog, goat, newt; drinks: coffee, kefir, milk, water. "Directly to the left of" means in the house numbered one lower; "next to" means in an adjacent house.

Clues:
1. The goat owner lives in house 2.
2. Bram lives in house 4.
3. The milk drinker lives in house 4.
4. The dog owner drinks water.
5. The kefir drinker lives directly to the left of the dog owner.
6. Ada does not own the dog.
7. The newt owner lives directly to the left of Dov.

Question: list the drinks in house order, from house 1 to house 4.

**Answer format:** the 4 drinks separated by commas, in house order 1 to 4

---

## Q29 · family: string-trace

Start with the string fgomjkrdswui. Apply the following operations in order. Positions are numbered from 1 at the left. Rotating left by one step moves the first letter to the end; rotating right by one step moves the last letter to the front.
1. Rotate left by 1 step.
2. Rotate left by 4 steps.
3. Reverse the letters in positions 8 through 9.
4. Reverse the letters in positions 3 through 6.
5. Swap the letters g and d (wherever they currently are).
6. Reverse the letters in positions 1 through 11.
7. Swap the letters u and r (wherever they currently are).
8. Remove the letter in position 12 and reinsert it so that it ends up in position 11.
9. Reverse the letters in positions 4 through 7.
10. Rotate right by 3 steps.
11. Rotate right by 4 steps.
12. Swap the letters m and d (wherever they currently are).
13. Swap the letters in positions 5 and 11.
14. Swap the letters k and d (wherever they currently are).
15. Rotate left by 4 steps.
16. Reverse the letters in positions 5 through 11.
17. Rotate left by 3 steps.
18. Rotate left by 1 step.
19. Reverse the letters in positions 1 through 9.
20. Reverse the letters in positions 6 through 9.
21. Remove the letter in position 6 and reinsert it so that it ends up in position 12.
22. Swap the letters in positions 12 and 10.
23. Reverse the letters in positions 1 through 5.
24. Swap the letters in positions 4 and 2.
25. Remove the letter in position 11 and reinsert it so that it ends up in position 4.
26. Swap the letters s and d (wherever they currently are).

Question: what is the final string?

**Answer format:** the final string (letters only)

---

## Q30 · family: logic-grid

4 people live in a row of 4 houses, numbered 1 to 4 from left to right. Each person has a different name and a house of a different colour. The possible values are: names: Bram, Fitz, Hana, Ivo; colours: black, green, white, yellow. "Directly to the left of" means in the house numbered one lower; "next to" means in an adjacent house.

Clues:
1. The resident of the black house lives in house 2.
2. The resident of the white house lives in house 4.
3. Bram does not live in the green house.
4. Bram does not live in the yellow house.
5. Fitz does not live in house 1.
6. The resident of the yellow house does not live in house 1.
7. Ivo lives in the black house.

Question: list the names in house order, from house 1 to house 4.

**Answer format:** the 4 names separated by commas, in house order 1 to 4

---

## Q31 · family: program-output

Predict exactly what this Python 3 program prints.

```python
total = 0
for i in range(1, 13):
    if i % 2 == 0:
        total += i * 5
    else:
        total -= 1
print(total)
```

**Answer format:** exactly the one line the program prints

---

## Q32 · family: logic-grid

5 people live in a row of 5 houses, numbered 1 to 5 from left to right. Each person has a different name, a house of a different colour and a different pet. The possible values are: names: Ada, Bram, Cleo, Dov, Gus; colours: black, grey, orange, red, white; pets: cat, crow, goat, newt, owl. "Directly to the left of" means in the house numbered one lower; "next to" means in an adjacent house.

Clues:
1. The cat owner is Gus.
2. The owl owner does not live next to Ada.
3. The resident of the grey house does not live next to the resident of the white house.
4. The cat owner does not live in house 5.
5. The owl owner does not live in house 4.
6. Dov lives in one of the two end houses.
7. Bram lives somewhere to the left of Ada.
8. The resident of the black house does not live next to Ada.
9. The resident of the white house lives in one of the two end houses.
10. The crow owner does not live in the grey house.
11. The newt owner lives somewhere to the left of Cleo.
12. The owl owner does not live next to the resident of the white house.
13. The resident of the grey house lives somewhere to the left of Ada.
14. The goat owner lives next to Ada.
15. The resident of the grey house does not live next to Bram.
16. The newt owner lives in one of the two end houses.
17. The resident of the orange house is Dov.
18. The resident of the grey house does not live in house 2.

Question: list the names in house order, from house 1 to house 5.

**Answer format:** the 5 names separated by commas, in house order 1 to 5

---

## Q33 · family: rule-inference

Each line below shows an input list of integers and the output list that a hidden rule produces from it. The same rule is used on every line.
[0, 3, 9, 8, 7, 4, 5, 12] → [3, 6, 12, 11, 10, 7, 8]
[9, 8, 3, 8, 6, 3, 2] → [12, 11, 6, 11, 9, 6]
[8, 2, 9, 2, 6, 1] → [11, 5, 12, 5, 9]
[2, 1, 12, 0, 5] → [5, 4, 15, 3]
[7, 12, 3, 10, 0, 4, 8, 12] → [10, 15, 6, 13, 3, 7, 11]

Question: what output does the rule produce for the input [2, 9, 11, 10, 12]?

**Answer format:** a list of integers in square brackets

---

## Q34 · family: string-trace

Start with the string lacusydorp. Apply the following operations in order. Positions are numbered from 1 at the left. Rotating left by one step moves the first letter to the end; rotating right by one step moves the last letter to the front.
1. Rotate right by 1 step.
2. Rotate left by 4 steps.
3. Rotate left by 3 steps.
4. Swap the letters u and o (wherever they currently are).
5. Swap the letters u and p (wherever they currently are).
6. Remove the letter in position 2 and reinsert it so that it ends up in position 8.
7. Swap the letters d and r (wherever they currently are).
8. Rotate left by 4 steps.
9. Remove the letter in position 10 and reinsert it so that it ends up in position 7.
10. Rotate left by 4 steps.
11. Swap the letters d and u (wherever they currently are).
12. Reverse the letters in positions 4 through 6.
13. Swap the letters in positions 10 and 1.
14. Swap the letters o and r (wherever they currently are).
15. Rotate left by 3 steps.
16. Reverse the letters in positions 7 through 8.

Question: what is the final string?

**Answer format:** the final string (letters only)

---

## Q35 · family: exact-computation

Compute the greatest common divisor of 10286 and 9472.

**Answer format:** a single integer (digits only)

---

## Q36 · family: exact-computation

A path goes from (0,0) to (10,10) using unit steps, each of which increases either the x-coordinate or the y-coordinate by 1, and it never visits a point with y > x. How many such paths pass through none of the points (2,1), (5,3), (7,4), (10,7)?

**Answer format:** a single integer (digits only)

---

## Q37 · family: rule-inference

Each line below shows an input list of integers and the output list that a hidden rule produces from it. The same rule is used on every line.
[2, 4, 2, 4, 11] → [16, 121, 4]
[7, 7, 2, 7, 6, 5, 12] → [4, 36, 25, 144, 49]
[8, 10, 5, 0, 8, 8, 9] → [100, 25, 0, 81, 64]
[7, 11, 12, 2, 12, 7, 9] → [121, 144, 4, 81, 49]
[9, 11, 8, 6, 4, 9, 3, 8] → [121, 64, 36, 16, 9, 81]
[0, 9, 7, 12, 4, 10, 2] → [81, 49, 144, 16, 100, 4, 0]

Question: what output does the rule produce for the input [4, 1, 11, 5, 2, 12]?

**Answer format:** a list of integers in square brackets

---

## Q38 · family: rule-inference

Each line below shows an input list of integers and the output list that a hidden rule produces from it. The same rule is used on every line.
[11, 2, 8, 2, 12, 0] → [35, 11, 13, 21, 23, 35]
[6, 10, 7, 0, 1] → [24, 6, 16, 23, 23]
[3, 1, 1, 0, 10, 10] → [25, 3, 4, 5, 5, 15]
[3, 4, 11, 2, 3, 10, 5] → [38, 3, 7, 18, 20, 23, 33]
[7, 6, 2, 12, 5, 5, 12] → [49, 7, 13, 15, 27, 32, 37]

Question: what output does the rule produce for the input [3, 1, 10, 1, 5]?

**Answer format:** a list of integers in square brackets

---

## Q39 · family: exact-computation

Compute 5696982400532 × 203952330124.

**Answer format:** a single integer (digits only)

---

## Q40 · family: string-trace

Start with the string tmcukw. Apply the following operations in order. Positions are numbered from 1 at the left. Rotating left by one step moves the first letter to the end; rotating right by one step moves the last letter to the front.
1. Rotate left by 2 steps.
2. Reverse the letters in positions 2 through 3.
3. Rotate left by 4 steps.
4. Reverse the letters in positions 1 through 5.
5. Swap the letters in positions 2 and 6.
6. Reverse the letters in positions 1 through 5.

Question: what is the final string?

**Answer format:** the final string (letters only)

---

## Q41 · family: logic-grid

5 people live in a row of 5 houses, numbered 1 to 5 from left to right. Each person has a different name, a different pet and a house of a different colour. The possible values are: names: Ada, Bram, Cleo, Gus, Ivo; pets: dog, fox, goat, hare, newt; colours: black, green, orange, red, yellow. "Directly to the left of" means in the house numbered one lower; "next to" means in an adjacent house.

Clues:
1. The resident of the black house lives directly to the left of the resident of the green house.
2. The resident of the red house is not Ivo.
3. The resident of the green house does not own the newt.
4. The dog owner lives directly to the left of Cleo.
5. The goat owner does not live in the black house.
6. Ada lives in one of the two end houses.
7. The resident of the green house does not live in house 4.
8. The resident of the red house lives somewhere to the left of the newt owner.
9. The hare owner is not Ada.
10. Ada lives directly to the left of Ivo.
11. The goat owner does not live in house 5.
12. Bram does not live in house 5.
13. Ivo lives next to Gus.
14. Ivo does not live next to the goat owner.
15. The resident of the orange house lives next to the resident of the black house.

Question: list the colours in house order, from house 1 to house 5.

**Answer format:** the 5 colours separated by commas, in house order 1 to 5

---

## Q42 · family: stock-log

Read this stock log and answer the question.

Rules for reading the log:
- Every entry is an accurate record, except that a CORRECTION replaces the quantity stated in the entry it names (the correction applies wherever it appears in the log).
- Stock changes only through the deliveries, shipments and transfers recorded here.
- Entries are in time order. A stocktake states the exact stock at the end of that day.

Opening stock (start of Day 1): Canal Store: 20 crates of lamp oil.

#1 Day 1: 11 crates of lamp oil shipped out from Canal Store.
#2 Day 1: 25 crates of lamp oil delivered to Canal Store.
#3 Day 2: the gate lock at Canal Store was replaced.
#4 Day 2: stocktake: Canal Store holds 34 crates of lamp oil.
#5 Day 3: 7 crates of lamp oil delivered to Canal Store.
#6 Day 4: 7 crates of lamp oil shipped out from Canal Store.
#7 Day 4: the gate lock at Canal Store was replaced.
#8 Day 4: stocktake: Canal Store holds 34 crates of lamp oil.
#9 Day 5: 40 crates of lamp oil delivered to Canal Store.
#10 Day 5: 19 crates of lamp oil shipped out from Canal Store.
#11 Day 5: a delivery of lamp oil arrived at Canal Store; the number of crates was not recorded.

Question: how many crates of lamp oil were in Canal Store at the end of Day 4?
Answer with a whole number of crates; or CONTRADICTORY if statements in the log that bear on this number cannot all be true; or NOT DETERMINABLE if the log does not contain enough information to fix the number.

**Answer format:** a whole number, or CONTRADICTORY, or NOT DETERMINABLE

---

## Q43 · family: exact-computation

Compute the sum of all positive divisors of 483600 (including 1 and 483600 itself).

**Answer format:** a single integer (digits only)

---

## Q44 · family: exact-computation

A path goes from (0,0) to (7,6) using unit steps, each of which increases either the x-coordinate or the y-coordinate by 1. How many such paths pass through none of the points (0,5), (3,4), (6,5)?

**Answer format:** a single integer (digits only)

---

## Q45 · family: program-output

Predict exactly what this Python 3 program prints.

```python
words = "crest delta fjord ember amber flint echo atlas delta".split()
counts = {}
for w in words:
    counts[w[0]] = counts.get(w[0], 0) + len(w)
print(",".join(k + str(v) for k, v in sorted(counts.items())))
```

**Answer format:** exactly the one line the program prints

---

## Q46 · family: logic-grid

4 people live in a row of 4 houses, numbered 1 to 4 from left to right. Each person has a different name and a house of a different colour. The possible values are: names: Bram, Esme, Fitz, Hana; colours: black, green, red, yellow. "Directly to the left of" means in the house numbered one lower; "next to" means in an adjacent house.

Clues:
1. Hana lives in house 2.
2. The resident of the green house lives next to Fitz.
3. The resident of the yellow house lives directly to the left of the resident of the black house.
4. Esme lives in house 1.
5. Bram does not live in the green house.

Question: list the colours in house order, from house 1 to house 4.

**Answer format:** the 4 colours separated by commas, in house order 1 to 4

---

## Q47 · family: string-trace

A rewriting process starts from the string CCAAACC and uses these rules:
Rule 1: AA → A
Rule 2: C → CA

One step: find the lowest-numbered rule whose left-hand side occurs somewhere in the current string, and replace the leftmost occurrence of that left-hand side with the rule's right-hand side. (Only one replacement is made per step.)

Question: what is the string after exactly 16 steps?

**Answer format:** the resulting string (letters only)

---

## Q48 · family: exact-computation

How many integers n with 1 ≤ n ≤ 85581 are divisible by none of 3, 5 and 11?

**Answer format:** a single integer (digits only)

---

## Q49 · family: exact-computation

Compute 42985572 × 6402966.

**Answer format:** a single integer (digits only)

---

## Q50 · family: exact-computation

Compute the remainder when 11^71 (that is, 11 raised to the power 71) is divided by 43.

**Answer format:** a single integer (digits only)

---

## Q51 · family: string-trace

A rewriting process starts from the string CCBCCC and uses these rules:
Rule 1: BB → (empty string)
Rule 2: CC → BB
Rule 3: AB → B
Rule 4: B → ABA

One step: find the lowest-numbered rule whose left-hand side occurs somewhere in the current string, and replace the leftmost occurrence of that left-hand side with the rule's right-hand side. (Only one replacement is made per step.)

Question: what is the string after exactly 26 steps?

**Answer format:** the resulting string (letters only)

---

## Q52 · family: stock-log

Read this stock log and answer the question.

Rules for reading the log:
- Every entry is an accurate record, except that a CORRECTION replaces the quantity stated in the entry it names (the correction applies wherever it appears in the log).
- Stock changes only through the deliveries, shipments and transfers recorded here.
- Entries are in time order. A stocktake states the exact stock at the end of that day.

Opening stock (start of Day 1): North Yard: 54 crates of nails.

#1 Day 1: 12 crates of nails delivered to North Yard.
#2 Day 1: stocktake: North Yard holds 66 crates of nails.
#3 Day 2: 5 crates of nails delivered to North Yard.
#4 Day 2: 28 crates of nails shipped out from North Yard.
#5 Day 3: 7 crates of nails delivered to North Yard.
#6 Day 3: the gate lock at North Yard was replaced.
#7 Day 3: a delivery of nails arrived at North Yard; the number of crates was not recorded.
#8 Day 4: 32 crates of nails delivered to North Yard.
#9 Day 4: 28 crates of nails delivered to North Yard.
#10 Day 5: 129 crates of nails shipped out from North Yard.
#11 Day 5: stocktake: North Yard holds 4 crates of nails.

Question: how many crates of nails were in North Yard at the end of Day 3?
Answer with a whole number of crates; or CONTRADICTORY if statements in the log that bear on this number cannot all be true; or NOT DETERMINABLE if the log does not contain enough information to fix the number.

**Answer format:** a whole number, or CONTRADICTORY, or NOT DETERMINABLE

---

## Q53 · family: logic-grid

3 people live in a row of 3 houses, numbered 1 to 3 from left to right. Each person has a different name and a different instrument. The possible values are: names: Ada, Esme, Ivo; instruments: cello, harp, violin. "Directly to the left of" means in the house numbered one lower; "next to" means in an adjacent house.

Clues:
1. Esme lives directly to the left of the harpist.
2. Esme does not play the violin.
3. The harpist is Ivo.
4. The harpist lives directly to the left of Ada.

Question: list the instruments in house order, from house 1 to house 3.

**Answer format:** the 3 instruments separated by commas, in house order 1 to 3

---

## Q54 · family: program-output

Predict exactly what this Python 3 program prints.

```python
xs = [2, 21, 33, 36, 4, 6, 29, 11, 5, 32]
ys = sorted(x % 8 for x in xs if x > 8)
print(ys[1:-1], sum(ys))
```

**Answer format:** exactly the one line the program prints

---

## Q55 · family: string-trace

A rewriting process starts from the string AABA and uses these rules:
Rule 1: AA → BA
Rule 2: A → BBA

One step: find the lowest-numbered rule whose left-hand side occurs somewhere in the current string, and replace the leftmost occurrence of that left-hand side with the rule's right-hand side. (Only one replacement is made per step.)

Question: what is the string after exactly 6 steps?

**Answer format:** the resulting string (letters only)

---

## Q56 · family: rule-inference

Each line below shows an input list of integers and the output list that a hidden rule produces from it. The same rule is used on every line.
[10, 9, 5, 9, 11] → [11, 10, 9, 5, 9]
[7, 9, 12, 6, 9] → [9, 7, 9, 12, 6]
[9, 5, 4, 6, 8, 8, 4] → [4, 9, 5, 4, 6, 8, 8]
[10, 12, 0, 6, 6, 12] → [12, 10, 12, 0, 6, 6]

Question: what output does the rule produce for the input [5, 12, 11, 11, 8, 7]?

**Answer format:** a list of integers in square brackets

---

## Q57 · family: rule-inference

Each line below shows an input list of integers and the output list that a hidden rule produces from it. The same rule is used on every line.
[12, 10, 12, 1, 0, 4, 7] → [19, 4, 11, 13, 1, 22, 22]
[7, 4, 11, 6, 0, 3] → [3, 10, 17, 6, 11, 15]
[3, 9, 2, 5, 2, 8] → [10, 11, 7, 7, 12, 11]
[7, 11, 7, 6, 2, 7, 5] → [12, 9, 12, 13, 8, 18, 18]
[0, 7, 1, 2, 7] → [7, 3, 9, 7, 8]
[6, 4, 5, 8, 7] → [13, 13, 15, 10, 9]

Question: what output does the rule produce for the input [3, 8, 10, 5, 2, 9, 2, 2]?

**Answer format:** a list of integers in square brackets

---

## Q58 · family: logic-grid

5 people live in a row of 5 houses, numbered 1 to 5 from left to right. Each person has a different name, a house of a different colour, a different pet and a different drink. The possible values are: names: Ada, Bram, Cleo, Hana, Ivo; colours: blue, orange, red, white, yellow; pets: dog, fox, hare, newt, owl; drinks: cocoa, coffee, kefir, tea, water. "Directly to the left of" means in the house numbered one lower; "next to" means in an adjacent house.

Clues:
1. Ivo lives next to the resident of the yellow house.
2. The hare owner lives directly to the left of the cocoa drinker.
3. The dog owner lives somewhere to the left of Bram.
4. The kefir drinker does not live next to the tea drinker.
5. The cocoa drinker does not live in house 2.
6. The resident of the red house lives next to the resident of the yellow house.
7. The coffee drinker lives directly to the left of the cocoa drinker.
8. The owl owner is Hana.
9. The resident of the blue house lives somewhere to the left of the water drinker.
10. The newt owner drinks water.
11. The dog owner lives next to the newt owner.
12. Bram lives somewhere to the left of Ada.
13. The resident of the red house does not drink kefir.
14. The resident of the orange house lives directly to the left of the dog owner.
15. The resident of the blue house does not live in house 1.

Question: list the pets in house order, from house 1 to house 5.

**Answer format:** the 5 pets separated by commas, in house order 1 to 5

---

## Q59 · family: logic-grid

4 people live in a row of 4 houses, numbered 1 to 4 from left to right. Each person has a different name, a different pet and a house of a different colour. The possible values are: names: Ada, Esme, Fitz, Ivo; pets: cat, crow, hare, owl; colours: black, grey, red, yellow. "Directly to the left of" means in the house numbered one lower; "next to" means in an adjacent house.

Clues:
1. Ivo lives in house 4.
2. The owl owner lives next to the resident of the black house.
3. The resident of the black house lives in house 1.
4. The resident of the yellow house does not live in house 4.
5. Ivo does not live in the grey house.
6. The resident of the yellow house does not live in house 3.
7. The resident of the yellow house is not Ada.
8. Fitz does not live in house 3.
9. Ada does not live in the grey house.
10. The hare owner lives in house 3.
11. The cat owner lives in house 4.

Question: list the names in house order, from house 1 to house 4.

**Answer format:** the 4 names separated by commas, in house order 1 to 4

---

## Q60 · family: rule-inference

Each line below shows an input list of integers and the output list that a hidden rule produces from it. The same rule is used on every line.
[5, 0, 10, 6, 4, 9] → [8, 3, 13, 9, 7, 12]
[2, 10, 5, 12, 12, 4, 8, 8] → [5, 13, 8, 15, 15, 7, 11, 11]
[11, 7, 2, 8, 1, 3, 0, 12] → [14, 10, 5, 11, 4, 6, 3, 15]
[12, 4, 5, 1, 4, 8, 8] → [15, 7, 8, 4, 7, 11, 11]

Question: what output does the rule produce for the input [9, 0, 2, 7, 8, 11, 6]?

**Answer format:** a list of integers in square brackets

---
