package com.topai.incidenciasestacionamiento.dto.response;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class AutomovilResponseDTO {
    private Long id;
    private String matricula;
    private String marca;
    private String modelo;
    private int year;
    private PropietarioResponseDTO propietario;
}
