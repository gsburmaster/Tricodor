import circuitgraph as cg




dff = [cg.BlackBox("dff", ["CK", "D"], ["Q"])]
c = cg.from_file('benchmarks/edited_benchmarks/s27.v', blackboxes=dff)
