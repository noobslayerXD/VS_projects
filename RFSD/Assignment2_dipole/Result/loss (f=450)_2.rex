<?xml version="1.0" encoding="UTF-8"?>
<MetaResultFile version="20211011" creator="SolverPP secondary quantity evaluation">
  <MetaGeometryFile filename="model.gex" lod="1"/>
  <SimulationProperties fieldname="loss (f=450)" frequency="450" encoded_unit="&amp;U:W^1.:m^-3" quantity="loss_density" fieldtype="Power Loss Density" fieldscaling="RMS" dB_Amplitude="10" excitation="2">
    <PrimaryResults>
      <PrimaryResult name="e-field (f=450)_2,1_m3d.rex"/>
    </PrimaryResults>
  </SimulationProperties>
  <ResultDataType vector="0" complex="0" timedomain="0" frequencymap="0"/>
  <SimulationDomain min="-284.913513 -134.913528 -124.913521" max="284.913513 134.913528 127.788521"/>
  <PlotSettings Plot="4" ignore_symmetry="0" deformation="0" enforce_culling="0" integer_values="0" combine="CombineNone" default_arrow_type="ARROWS" default_scaling="NONE"/>
  <Source type="POSTPROCESSING"/>
  <SpecialMaterials>
    <Background type="FIELDFREE"/>
    <Material name="$NFSMaterial$" type="FIELDFREE_HIDESURFACE"/>
    <Material name="$PortFaceMaterial$" type="FIELDFREE_HIDESURFACE"/>
    <Material name="$PortMaterial$" type="FIELDFREE_HIDESURFACE"/>
    <Material name="PEC" type="FIELDFREE_HIDESURFACE"/>
    <Material name="Vacuum" type="FIELDFREE_HIDESURFACE"/>
    <Material name="air_0" type="FIELDFREE_HIDESURFACE"/>
  </SpecialMaterials>
  <AuxGeometryFile/>
  <AuxResultFile/>
  <FieldFreeNodes/>
  <SurfaceFieldCoefficients/>
  <UnitCell/>
  <SubVolume/>
  <Units/>
  <ProjectUnits/>
  <TimeSampling/>
  <LocalAxes/>
  <MeshViewSettings/>
  <ResultGroups num_steps="1" transformation="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1" process_mesh_group="0">
    <SharedDataWith/>
    <Frame index="0">
      <PortModeInfoFile/>
      <FieldResultFile filename="loss (f=450)_2,1.m3d" type="m3d"/>
    </Frame>
  </ResultGroups>
  <AutoScale>
    <SmartScaling log_strength="1" log_anchor="0" log_anchor_type="0" db_range="40" phase="0"/>
  </AutoScale>
</MetaResultFile>
