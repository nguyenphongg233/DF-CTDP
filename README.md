# DF-CTDP
Experimental results for ALNS algorithm on territory design problem.

## Folder Structure

```
DF-CTDP/
├── README.md
├── 5.2 Mathematical formulation validation/
│   └── input/
├── 5.3. Performance of the ALNS algorithm on small instances/
│   ├── data.txt
│   ├── input/
│   └── output/
├── 5.4. Performance of the ALNS algorithm on large-scale instances/
│   ├── Table 6/
│   │   ├── data.txt
│   │   ├── input/
│   │   └── output/
│   └── Table 7+8/
│       ├── input/
│       ├── log/
│       └── output/
└── 5.5. Performance of the ALNS algorithm on real-world instances/
    ├── data.txt
    ├── input/
    ├── log/
    └── output/
```

## Directory Descriptions

### 5.2 Mathematical formulation validation/
- Validates the mathematical model on small test instances
- Verifies constraint implementation (capacity, balance, contiguity)
- **Contents**: `input/` - Validation instances

### 5.3 Small instances (60-100 basic units)
- Tests 2DU60, 2DU80, 2DU100 with 5-10 territories per instance
- 20 independent runs per configuration
- Instance format: `2DU{n}-{p}-{id}` (n: size, p: territories, id: 1-20)
- **Contents**: `input/`, `output/`, `data.txt`, `data.xlsx`

### 5.4 Large-scale instances

#### Table 6 (Planar graphs 500-700 nodes)
- Tests scalability on large synthetic instances (G0-G9 variations)
- Instance format: `planar{n}_G{id}` (n: 500, 600, 700)
- **Contents**: `input/`, `output/`, `data.txt`, `data.xlsx`

#### Table 7+8 (Algorithm variants)
- Compares different algorithm configurations
- Parameter sensitivity analysis
- **Contents**: `input/`, `output/`, `log/`

### 5.5 Real-world instances
- Region R1 (233 units, 33 territories) and R2 (175 units, 67 territories)
- Balance thresholds: T=0.05, T=0.1
- Format: `R{region}-DU{n}-P{p}-T{threshold}-{id}`
- **Contents**: `input/`, `output/`, `log/`, `data.txt`

## Data Format

File format in `data.txt`:
```
Instance {name} {iteration}  objective {total}  and values ({balance},{familiarity},{compactness})
```

Examples:
- Small instance: `Instance 2DU60-05-1 1  objective 5305.57  and values (0.00,0.00,5305.57)`
- Real-world: `Instance R1-DU233-P33-T0.1-0  objective 21041367.75  and values (20472.37,372.00,383002.30)`

Components:
- **balance**: Workload balance penalty (0.00 = perfectly balanced)
- **familiarity**: Territory reassignment cost (0.00 = no changes)
- **compactness**: Distance cost (sum of Euclidean distances)
