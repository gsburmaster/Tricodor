import circuitgraph as cg

dff = [cg.BlackBox("dff", ["CK", "D"], ["Q"])]
c = cg.from_file('benchmarks/basic.v', blackboxes=dff)
