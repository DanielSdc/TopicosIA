package com.topai.incidenciasestacionamiento.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class ErrorResponseDTO {
    private String mensaje;
    private LocalDateTime timestamp;
    private int codigoEstado;
}
