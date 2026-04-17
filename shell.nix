{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "yolo-vision-env";

  buildInputs = with pkgs; [
    python3
    python3Packages.pip
    python3Packages.ultralytics
    python3Packages.opencv4
    python3Packages.numpy
    
    # Dependencias de sistema para OpenCV y procesamiento de imagen
    libGL
    libGLU
    glib
    xorg.libX11
    xorg.libXext
    xorg.libXrender
    xorg.libICE
    xorg.libSM
  ];

  shellHook = ''
    export PYTHONWARNINGS="ignore"
    
    export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [
      pkgs.libGL
      pkgs.glib
      pkgs.xorg.libX11
    ]}:$LD_LIBRARY_PATH"

    clear
  '';
}
