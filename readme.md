# Heroes 3 battle API (poka chto)

## Calculating creature damage in **Heroes of Might and Magic 3 Horn of The Abyss**

The base damage of any creature, war machine or shooting turret is represented as a range from the lowest possible damage per creature to the highest possible damage. If a creature suffers more damage than its current health, it is eliminated, while in a stack of creatures, the topmost dies. The remainder of the damage is dealt to the next one and so forth until all damage is dealt or the whole stack is eliminated.

The total damage when attacking an enemy squad depends on the number of creatures in the attacking squad and many modifiers. In general, the formula of total damage is as follows:

$$D_{final}= D_{base} * (1 + MD_1 + M_{attack} + M_{specialization} + M_{luck} + M_{ability}) * (1 - MD_2) * (1 - M_{armourer}) * (1 - M_{spells}) * (1 - M_{penalty}) * (1 - M_{def})$$

In our case, when only unit stats are taken into account, the formula will look like:

$$D_{final}= D_{base} * (1 + MD_1 + M_{luck}) * (1 - MD_2)$$

### 1. BASIC DAMAGE – variable D<sub>base</sub>

Each creature has a certain range of damage values [D<sub>min</sub> ... D<sub>max</sub>] displayed in its stats. Base damage for a stack of creatures is calculated as such:

* If there are less than or equal to 10 creatures in a stack then a random integer is chosen in a damage range for each creature, and they are added up.

* If there are more than 10 creatures in a stack, 10 random integers are chosen in a damage range of the creature and added up. The result is multiplied by **N/10**, where **N** is the number of creatures in the stack, and rounded down.

### 2. Attack-Defense difference – variables MD<sub>1</sub> and MD<sub>2</sub>

The Attack-Defense difference (ADD), denoted by MD<sub>1</sub> and MD<sub>2</sub> in the formula, is typically the main modifier of the base damage.  It is calculated as the difference between the attacker's attack value and the defender's defense value.  
In the formula the MD modifier occurs twice: 1 is used when the attacker's Attack is greater than the target's Defense (MD<sub>2</sub> is equal to 1). MD<sub>2</sub> is used when the target's Defense is greater than the attacker's Attack (MD<sub>1</sub> is 0).

$MD_1 = 0,05 * (Attack- Defense)$,  if Attack > Defense, otherwise 0

$MD_2 = 0,025 * (Attack- Defense)$,  if Defense > Attack, otherwise 0

Each point of attacking Stack Attack that exceeds the target's Defense increases the total damage by **5%** of the base damage. However, the damage modifier cannot exceed the value of 3 (**+300%** to base damage). The maximum effective difference between Attack and Defense is **60**.
Each point of Target Defense that exceeds the attacking Stack's Attack reduces the resulting damage by **2.5%** of the base damage. However, the damage modifier cannot be lower than 0.3 (**-70%** to base damage). The maximum effective difference between Defense and Attack is **28**.

## Endpoitns

### 1. Unit/Stack information

- **Endpoint**: `/unit`
* **Method**: `GET`
* **Description**: returns all information about unit, including non-battle one
* **Required query params**:

| Param |                 Description                  | Example value |
| :---: | :------------------------------------------: | :-----------: |
| name  | name of the unit, all lowercase, underscored |     nymph     |

* **Example request**:

`GET /unit?name=sea_dog`

* **Example response body**:

```json
{
    "name" : "Sea Dog",
    "town": "Coven",
    "lvl": {"base": 3, "upgrade": 2},
    "attack": 12,
    "defence": 11,
    "min_damage": 3,
    "max_damage": 7,
    "health" : 15,
    "speed": 8,
    "growth": 7,
    "ai_value": 602,
    "cost": 375,
    "special": ["Ranged (12 shots)", "No melee penalty", "No enemy retaliation", "Accurate Shot"]
}
```

### 2. Stack information

* **Endpoint**: `/stack`
* **Method**: `GET`

* **Required query params**:

| Param |                  Description                   | Example value |
| :---: | :--------------------------------------------: | :-----------: |
| name  |  name of the unit, all lowercase, underscored  |  troglodyte   |
| count | amount of units in the stack, positive integer |      15       |

* **Example request**:

`GET /stack?name=minotaur&count=148`

* **Example response body**:

```json
{
    "name" : "Minotaur",
    "lvl": "5",
    "attack": 14,
    "defence": 12,
    "min_damage": 1776,
    "max_damage": 2960,
    "health" : 7400,
    "speed": 8,
    "special": ["Positive Morale"]
}
```

### 3. Quick battle

* **Endpoint**: `/quick-battle`
* **Method**: `POST`
* **Description**: returns approximation of battle resolve between 2 stacks. Distance between units is not taken into account. Attacker is the stack, that attacks first.

* **Example request body**:

```json
{
    "attacker_unit": "Minotaur",
    "attacker_unit_count": 13,
    "defender_unit": "Titan",
    "defender_unit_count": 2
}
```

* **Example response json**:

```json
{
    "winner": "Attacker",
    "winner_unit": "Minotaur",
    "winner_losses": 4,
    "loser_unit": "Titan",
    "loser_losses": 2,
    "experience": 600
}
```

## Unit information sources

For the reference we are using <https://heroes.thelazy.net/index.php/List_of_creatures_(HotA>)

**BASE_PATH** = //*[@id="mw-content-text"]/div/table/tbody/tr[n], where **n** is Natural Number

In the example table **n** = 3

| Charachteristic |          Description          |        Example value        |                             XPath                              |
| :-------------: | :---------------------------: | :-------------------------: | :------------------------------------------------------------: |
|      name       |       name of the unit        |           Oceanid           |                  BASE_PATH/td[1]/a[2]/text()                   |
|      town       |    hometown for this unit     |            Cove             |                  BASE_PATH/td[2]/span/@title                   |
|      level      |       level of the unit       |             1 +             | BASE_PATH/td[3]/span/text() \| BASE_PATH/td[3]/span/sup/text() |
|     attack      |    attack stat of the unit    |              6              |                  BASE_PATH/td[4]/span/text()                   |
|     defense     |   defense stat of the unit    |              2              |                  BASE_PATH/td[5]/span/text()                   |
|     min_dmg     |  minumum damage of the unit   |              1              |                  BASE_PATH/td[6]/span/text()                   |
|     max_dmg     |  maximum damage of the unit   |              3              |                  BASE_PATH/td[7]/span/text()                   |
|     health      |       healt of the unit       |              4              |                  BASE_PATH/td[8]/span/text()                   |
|      speed      |       speed of the unit       |              8              |                  BASE_PATH/td[9]/span/text()                   |
|     growth      |     unit growth per week      |             16              |                  BASE_PATH/td[10]/span/text()                  |
|    ai_value     |     AI value of the unit      |             75              |                  BASE_PATH/td[11]/span/text()                  |
|      cost       |       cost of the unit        |           45&nbsp           |                    BASE_PATH/td[12]/text()                     |
|     special     | special abilities of the unit | Teleporting , Immune to ice |                        BASE_PATH/td[14]                        |
