package com.topai.incidenciasestacionamiento.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import lombok.Data;

@Data
public class PropietarioRequestDTO {
    @NotBlank
    private String nombre;
    @NotBlank
    private String direccion;
    @Positive
    private Long usuarioId;
}
