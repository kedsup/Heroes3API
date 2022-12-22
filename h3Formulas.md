# Calculating creature damage in **Heroes of Might and Magic 3 Horn of The Abyss** 

The base damage of any creature, war machine or shooting turret is represented as a range from the lowest possible damage per creature to the highest possible damage. If a creature suffers more damage than its current health, it is eliminated, while in a stack of creatures, the topmost dies. The remainder of the damage is dealt to the next one and so forth until all damage is dealt or the whole stack is eliminated.

The total damage when attacking an enemy squad depends on the number of creatures in the attacking squad and many modifiers. In general, the formula of total damage is as follows:

$$D_{final}= D_{base} * (1 + MD_1 + M_{attack} + M_{specialization} + M_{luck} + M_{offence}) * (1 - MD_2) * (1 - M_{armourer}) * (1 - M_{spells}) * (1 - M_{penalty}) * (1 - M_{def})$$

## 1. BASIC DAMAGE D<sub>base</sub>

Each creature has a certain range of damage values [D<sub>min</sub> ... D<sub>max</sub>] displayed in its stats. Base damage for a stack of creatures is calculated as such:

* If there are less than or equal to 10 creatures in a stack then a random integer is chosen in a damage range for each creature, and they are added up.

* If there are more than 10 creatures in a stack, 10 random integers are chosen in a damage range of the creature and added up. The result is multiplied by **N/10**, where **N** is the number of creatures in the stack, and rounded down.

Only 3 factors (spells) can affect base damage:

* **Bless** - the base damage of the creature becomes equal to **D<sub>max</sub>**(or D<sub>max</sub>+1 with Advanced of Expert **Water Magic**).
  
* **Curse** -  the base damage of the creature becomes equal to **D<sub>min</sub>**(or D<sub>min</sub>-1 with Advanced of Expert **Fire Magic**). However, the damage dealt by the creature cannot be less than 1.

* **Forgetfulness** - technically reduces the number of creatures **N** in the attacking squad by 50%, rounding up.

## 2. Attack-Defense difference – variables MD<sub>1</sub> and MD<sub>2</sub>

The Attack-Defense difference, denoted by MD<sub>1</sub> and MD<sub>2</sub> in the formula, is typically the main modifier of the base damage.
