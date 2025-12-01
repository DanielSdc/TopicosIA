package com.topai.incidenciasestacionamiento.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import lombok.Data;

@Data
public class AutomovilRequestDTO {

    @NotBlank
    private String matricula;
    @Positive
    private Long propietario;
    @NotBlank
    private String marca;
    @NotBlank
    private String modelo;
    @Positive
    private int year;
}
