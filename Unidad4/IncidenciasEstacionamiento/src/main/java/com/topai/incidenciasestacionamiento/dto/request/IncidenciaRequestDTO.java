package com.topai.incidenciasestacionamiento.dto.request;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class IncidenciaRequestDTO {
    @NotNull
    @DecimalMin(value = "-180.00")
    @DecimalMax(value = "180.00")
    private Double longitud;

    @NotNull
    @DecimalMin(value = "-90.0")
    @DecimalMax(value = "90.0")
    private Double latitud;

    @NotBlank
    private String matricula;
}
