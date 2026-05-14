{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    fastapi
    uvicorn
    python-json-logger
    prometheus-client
  ]);
in

pkgs.stdenv.mkDerivation {
  pname = "devops-info-service";
  version = "1.0.0";

  src = ./.;

  nativeBuildInputs = [
    pkgs.makeWrapper
  ];

  installPhase = ''
    mkdir -p $out/bin
    mkdir -p $out/app

    cp app.py $out/app/

    cat > $out/bin/devops-info-service <<EOF
#!/usr/bin/env bash
cd $out/app
exec ${pythonEnv}/bin/uvicorn app:app --host 0.0.0.0 --port 5000
EOF

    chmod +x $out/bin/devops-info-service
  '';
}