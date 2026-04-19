# EarthSciModels

This repository Earth science model components implemented using the format described at https://github.com/EarthSciML/EarthSciSerialization/blob/main/esm-schema.json.

## Directory Layout

All model components should be placed in subdirectories of the `models/` top-level directory, with nested subdirectories organized according to the scientific domains of the model components they contain. 

## File contents 

Each model file should contain approximately all of the model components in an individual paper or chapter. Each component should start at version 0.1.0 and be incremented to 1.0.0 when a human maintainer is confident that it is scientifically correct. Each component should contain a description, a reference to the original published description, tests to verify its behavior, and examples to demonstrate its behavior, all contained within the single model file.
